"""Leave management API endpoints"""

from flask import Blueprint, request, jsonify
import uuid

leaves_bp = Blueprint('leaves', __name__)

@leaves_bp.route('/apply', methods=['POST'])
def apply_leave():
    """Apply for leave"""
    data = request.get_json()
    
    required_fields = ['employee_id', 'leave_type', 'start_date', 'end_date', 'reason']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    return jsonify({
        'id': str(uuid.uuid4()),
        'status': 'pending',
        'message': 'Leave request submitted successfully'
    }), 201

@leaves_bp.route('', methods=['GET'])
def list_leaves():
    """List leave requests"""
    return jsonify({
        'leaves': [
            {
                'id': str(uuid.uuid4()),
                'employee_id': 'EMP001',
                'leave_type': 'sick',
                'start_date': '2024-12-20',
                'end_date': '2024-12-22',
                'status': 'pending',
                'total_days': 3
            }
        ]
    }), 200

@leaves_bp.route('/<leave_id>/approve', methods=['PUT'])
def approve_leave(leave_id):
    """Approve leave request"""
    data = request.get_json()
    
    return jsonify({
        'id': leave_id,
        'status': 'approved',
        'message': 'Leave request approved'
    }), 200

@leaves_bp.route('/<leave_id>/reject', methods=['PUT'])
def reject_leave(leave_id):
    """Reject leave request"""
    data = request.get_json()
    
    if not data or not data.get('reason'):
        return jsonify({'error': 'Missing rejection reason'}), 400
    
    return jsonify({
        'id': leave_id,
        'status': 'rejected',
        'reason': data['reason'],
        'message': 'Leave request rejected'
    }), 200

@leaves_bp.route('/<leave_id>', methods=['GET'])
def get_leave(leave_id):
    """Get leave request details"""
    return jsonify({
        'leave': {
            'id': leave_id,
            'employee_id': 'EMP001',
            'leave_type': 'sick',
            'start_date': '2024-12-20',
            'end_date': '2024-12-22',
            'status': 'pending',
            'reason': 'Medical leave'
        }
    }), 200
