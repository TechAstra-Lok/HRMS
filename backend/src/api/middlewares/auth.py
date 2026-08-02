"""Authentication Middleware"""

from flask import request, g, jsonify
from functools import wraps
from src.core.security import jwt_manager
from models import User

def auth_middleware(f):
    """Authentication middleware decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization'].split()
            if len(auth_header) == 2:
                token = auth_header[1]
        
        if not token:
            return jsonify({'error': 'Missing authentication token'}), 401
        
        try:
            payload = jwt_manager.verify_token(token)
            user_id = payload.get('sub')
            g.user_id = user_id
            g.tenant_id = payload.get('tenant')
            g.roles = payload.get('roles', [])
            
            # Load user from database
            user = User.query.filter_by(id=user_id, is_deleted=False).first()
            if not user or not user.is_active:
                return jsonify({'error': 'User not found or inactive'}), 401
            
            g.user = user
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_permission(resource, action):
    """Permission checking decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from src.core.security import rbac_manager
            
            if not hasattr(g, 'roles'):
                return jsonify({'error': 'Unauthorized'}), 401
            
            # Check if any role has permission
            for role in g.roles:
                if rbac_manager.has_permission(role, resource, action):
                    return f(*args, **kwargs)
            
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        return decorated_function
    return decorator
