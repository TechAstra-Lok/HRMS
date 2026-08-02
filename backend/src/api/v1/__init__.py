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
    from ...models import User, Tenant, db

    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'email_and_password_required'}), 400

    user = User.query.filter_by(email=email, is_deleted=False).first()
    if not user or not hash_manager.verify_password(password, user.password_hash):
        return jsonify({'error': 'invalid_credentials'}), 401

    if not user.is_active:
        return jsonify({'error': 'user_inactive'}), 403

    roles = ['super_admin'] if user.is_super_admin else ['employee']
    access_token = jwt_manager.generate_access_token(str(user.id), str(user.tenant_id), roles)
    refresh_token = jwt_manager.generate_refresh_token(str(user.id))
    session_id = security_manager.create_session(str(user.id), str(user.tenant_id), roles)

    response = make_response(jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': str(user.id),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'roles': roles,
        },
        'tenant_id': str(user.tenant_id)
    }))
    response.set_cookie('session_id', session_id, httponly=True, secure=True, samesite='Lax', max_age=1800)
    return response

@auth_bp.route('/logout', methods=['POST'])
def logout():
    from flask import request, jsonify, make_response
    from src.core.security import security_manager

    session_id = request.cookies.get('session_id')
    if session_id:
        security_manager.revoke_session(session_id)

    response = make_response(jsonify({'message': 'Logged out successfully'}))
    response.delete_cookie('session_id')
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
    from flask import jsonify
    from ...models import Employee

    employees = Employee.query.filter_by(is_deleted=False).all()
    return jsonify({'employees': [e.to_dict() for e in employees]})

@employees_bp.route('', methods=['POST'])
def create_employee():
    from flask import request, jsonify
    from ...models import Employee, db
    import uuid

    data = request.get_json(silent=True) or {}
    employee = Employee(
        id=uuid.uuid4(),
        first_name=data.get('first_name', '').strip(),
        last_name=data.get('last_name', '').strip(),
        email=data.get('email', '').strip(),
        phone=data.get('phone', '').strip(),
        department=data.get('department', '').strip(),
        designation=data.get('designation', '').strip(),
        date_of_birth=data.get('date_of_birth'),
        join_date=data.get('join_date'),
        employee_id=data.get('employee_id', str(uuid.uuid4())[:8]),
        tenant_id=data.get('tenant_id')
    )

    db.session.add(employee)
    db.session.commit()
    return jsonify(employee.to_dict()), 201

@attendance_bp.route('/check-in', methods=['POST'])
def check_in():
    from flask import request, jsonify
    from ...models import Attendance, db
    from datetime import datetime
    import uuid

    data = request.get_json(silent=True) or {}
    attendance = Attendance(
        id=uuid.uuid4(),
        employee_id=data.get('employee_id'),
        date=datetime.utcnow().date(),
        check_in=datetime.utcnow(),
        check_in_latitude=data.get('latitude'),
        check_in_longitude=data.get('longitude'),
        status='present',
        tenant_id=data.get('tenant_id')
    )

    db.session.add(attendance)
    db.session.commit()
    return jsonify(attendance.to_dict()), 201

@attendance_bp.route('/check-out', methods=['POST'])
def check_out():
    from flask import request, jsonify
    from ...models import Attendance, db
    from datetime import datetime

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
    from ...models import Employee, Attendance, LeaveRequest
    from datetime import date

    total_employees = Employee.query.filter_by(is_deleted=False).count()
    today_attendance = Attendance.query.filter_by(date=date.today()).count()
    pending_leaves = LeaveRequest.query.filter_by(status='pending').count()

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
