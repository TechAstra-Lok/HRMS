"""API v1 module"""

from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
employees_bp = Blueprint('employees', __name__)
attendance_bp = Blueprint('attendance', __name__)
leaves_bp = Blueprint('leaves', __name__)
payroll_bp = Blueprint('payroll', __name__)
dashboard_bp = Blueprint('dashboard', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    from flask import request, jsonify, make_response
    from src.core.security import hash_manager, jwt_manager, security_manager

    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not email or not password:
        return jsonify({'error': 'email_and_password_required'}), 400

    demo_user = {
        'id': 'demo-admin',
        'tenant_id': 'demo-tenant',
        'email': 'admin@hrms.local',
        'first_name': 'Demo',
        'last_name': 'Administrator',
        'password_hash': hash_manager.hash_password('Demo@1234'),
        'is_active': True,
        'is_super_admin': True,
        'is_deleted': False,
    }

    if email == demo_user['email'] and hash_manager.verify_password(password, demo_user['password_hash']):
        user = demo_user
    else:
        return jsonify({'error': 'invalid_credentials'}), 401

    roles = ['super_admin'] if user['is_super_admin'] else ['employee']
    access_token = jwt_manager.generate_access_token(str(user['id']), str(user['tenant_id']), roles)
    refresh_token = jwt_manager.generate_refresh_token(str(user['id']))
    session_id = security_manager.create_session(str(user['id']), str(user['tenant_id']), roles)

    response = make_response(jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': str(user['id']),
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'roles': roles,
        },
        'tenant_id': str(user['tenant_id'])
    }))
    response.set_cookie('session_id', session_id, httponly=True, secure=False, samesite='Lax', max_age=1800)
    return response

@auth_bp.route('/logout', methods=['POST'])
def logout():
    from flask import request, jsonify, make_response
    from src.core.security import security_manager

    session_id = request.cookies.get('session_id')
    if session_id:
        security_manager.revoke_session(session_id)

    response = make_response(jsonify({'message': 'Logged out successfully'}))
    response.delete_cookie('session_id', secure=False)
    return response

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    from flask import request, jsonify
    from src.core.security import jwt_manager
    from ...models import User

    auth_header = request.headers.get('Authorization', '')
    token = auth_header.split(' ')[-1] if auth_header.startswith('Bearer ') else None
    if not token:
        return jsonify({'error': 'missing_refresh_token'}), 401

    try:
        payload = jwt_manager.verify_token(token)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 401

    if payload.get('type') != 'refresh':
        return jsonify({'error': 'invalid_token_type'}), 401

    user_id = payload.get('sub')
    user = User.query.filter_by(id=user_id, is_deleted=False).first()
    if not user:
        return jsonify({'error': 'user_not_found'}), 404

    new_access_token = jwt_manager.generate_access_token(str(user.id), str(user.tenant_id), payload.get('roles', ['employee']))
    return jsonify({'access_token': new_access_token})

@employees_bp.route('', methods=['GET'])
def list_employees():
    from flask import jsonify, current_app
    import json
    import os

    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    data_file = os.path.join(data_dir, 'employees.json')
    try:
        with open(data_file, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
    except Exception:
        payload = {'employees': []}

    return jsonify(payload)

@employees_bp.route('', methods=['POST'])
def create_employee():
    from flask import request, jsonify
    import json
    import os
    import uuid
    from flask import current_app

    data = request.get_json(silent=True) or {}
    new_emp = {
        'id': str(uuid.uuid4()),
        'first_name': data.get('first_name', '').strip(),
        'last_name': data.get('last_name', '').strip(),
        'email': data.get('email', '').strip(),
        'phone': data.get('phone', '').strip(),
        'department': data.get('department', '').strip() or 'Operations',
        'designation': data.get('designation', '').strip() or 'Employee',
        'employee_id': data.get('employee_id') or str(uuid.uuid4())[:8],
        'tenant_id': data.get('tenant_id') or 'demo-tenant'
    }

    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    os.makedirs(data_dir, exist_ok=True)
    data_file = os.path.join(data_dir, 'employees.json')

    try:
        with open(data_file, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
    except Exception:
        payload = {'employees': []}

    payload['employees'].append(new_emp)

    with open(data_file, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=2)

    return jsonify(new_emp), 201

@attendance_bp.route('/check-in', methods=['POST'])
def check_in():
    from flask import jsonify, current_app
    import json
    import os
    from datetime import date

    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    data_file = os.path.join(data_dir, 'employees.json')
    try:
        with open(data_file, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
            total_employees = len(payload.get('employees', []))
    except Exception:
        total_employees = 0

    # Count today's attendance from attendances file if present
    attend_file = os.path.join(data_dir, 'attendances.json')
    today_attendance = 0
    try:
        with open(attend_file, 'r', encoding='utf-8') as fh:
            attend = json.load(fh)
            today = date.today().isoformat()
            today_attendance = sum(1 for a in attend.get('attendances', []) if a.get('date') == today)
    except Exception:
        today_attendance = 0

    leave_file = os.path.join(data_dir, 'leave_requests.json')
    pending_leaves = 0
    try:
        with open(leave_file, 'r', encoding='utf-8') as fh:
            leaves = json.load(fh)
            pending_leaves = sum(1 for l in leaves.get('leave_requests', []) if l.get('status') == 'pending')
    except Exception:
        pending_leaves = 0

    return jsonify({
        'total_employees': total_employees,
        'today_attendance': today_attendance,
        'pending_leaves': pending_leaves,
        'monthly_payroll': 0,
        'attendance_chart': {
            'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            'present': [45, 48, 50, 47, 46],
            'absent': [2, 1, 0, 2, 1],
            'late': [3, 1, 2, 1, 3]
        },
        'department_chart': {
            'labels': ['IT', 'HR', 'Finance', 'Operations'],
            'data': [30, 20, 25, 25]
        },
        'recent_activities': [],
        'visualization_data': {'attendance': []}
    })

    data = request.get_json(silent=True) or {}
    employee_id = data.get('employee_id')
    if not employee_id:
        return jsonify({'error': 'employee_id_required'}), 400

    attendance = Attendance.query.filter_by(
        employee_id=employee_id,
        date=datetime.utcnow().date()
    ).first()
    if not attendance:
        return jsonify({'error': 'no_checkin_record'}), 404

    attendance.check_out = datetime.utcnow()
    db.session.commit()
    return jsonify(attendance.to_dict())

@dashboard_bp.route('/stats', methods=['GET'])
def get_stats():
    from flask import jsonify

    return jsonify({
        'total_employees': 3,
        'today_attendance': 2,
        'pending_leaves': 1,
        'monthly_payroll': 125000,
        'attendance_chart': {
            'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            'present': [45, 48, 50, 47, 46],
            'absent': [2, 1, 0, 2, 1],
            'late': [3, 1, 2, 1, 3]
        },
        'department_chart': {
            'labels': ['IT', 'HR', 'Finance', 'Operations'],
            'data': [30, 20, 25, 25]
        },
        'recent_activities': [
            {'action': 'Demo login', 'detail': 'Admin signed in successfully'},
            {'action': 'Payroll synced', 'detail': 'Monthly payroll prepared for review'}
        ],
        'visualization_data': {'attendance': []}
    })

@leaves_bp.route('/apply', methods=['POST'])
def apply_leave():
    from flask import request, jsonify
    from ...models import LeaveRequest, db
    import uuid

    data = request.get_json(silent=True) or {}
    leave = LeaveRequest(
        id=uuid.uuid4(),
        employee_id=data.get('employee_id'),
        leave_type=data.get('leave_type'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        total_days=data.get('total_days'),
        reason=data.get('reason'),
        status='pending',
        tenant_id=data.get('tenant_id')
    )

    db.session.add(leave)
    db.session.commit()
    return jsonify(leave.to_dict()), 201

@payroll_bp.route('/calculate', methods=['POST'])
def calculate_payroll():
    from flask import request, jsonify

    data = request.get_json(silent=True) or {}
    return jsonify({
        'message': 'Payroll calculation started',
        'month': data.get('month'),
        'year': data.get('year')
    })
