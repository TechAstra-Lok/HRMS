"""Authentication, authorization, and MFA utilities."""

import re
import uuid
import pyotp
from functools import wraps
from datetime import datetime
from typing import Optional
from flask import request, jsonify, g
from .jwt import jwt_manager
from .rbac import rbac_manager
from .session_manager import session_manager
from src.exceptions import AuthenticationError, AuthorizationError, ValidationError
from src.models import User


class SecurityManager:
    """Security operations and policy enforcement."""

    PASSWORD_POLICY = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,}$'
    )

    def validate_password_policy(self, password: str) -> None:
        if not password or not self.PASSWORD_POLICY.match(password):
            raise ValidationError(
                'Password must be at least 12 characters and include uppercase, lowercase, number, and special character.'
            )

    def generate_mfa_secret(self) -> str:
        return pyotp.random_base32()

    def get_mfa_uri(self, secret: str, email: str, issuer: str = 'Enterprise HRMS') -> str:
        return pyotp.totp.TOTP(secret).provisioning_uri(email, issuer_name=issuer)

    def validate_mfa_code(self, secret: str, code: str) -> bool:
        if not secret or not code:
            return False
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)

    def create_session(self, user_id: str, tenant_id: str, roles: list) -> str:
        session_id = str(uuid.uuid4())
        session_manager.create_session(session_id, user_id, tenant_id, roles)
        return session_id

    def validate_session(self, session_id: str) -> Optional[dict]:
        return session_manager.validate_session(session_id)

    def revoke_session(self, session_id: str) -> None:
        session_manager.revoke_session(session_id)


security_manager = SecurityManager()


def require_auth(f):
    """Decorator to enforce access token authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token = None
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ', 1)[1].strip()
        if not token:
            raise AuthenticationError('Missing authentication token.')

        try:
            payload = jwt_manager.verify_token(token)
        except ValueError as exc:
            raise AuthenticationError(str(exc))

        if payload.get('type') != 'access':
            raise AuthenticationError('Invalid token type.')

        user_id = payload.get('sub')
        user = User.query.filter_by(id=user_id, is_deleted=False).first()
        if not user or not user.is_active:
            raise AuthenticationError('User account is inactive or not found.')

        g.user_id = user_id
        g.tenant_id = payload.get('tenant')
        g.roles = payload.get('roles', [])
        g.user = user

        session_id = request.cookies.get('session_id')
        if session_id:
            session_data = session_manager.validate_session(session_id)
            if session_data and session_data.get('user_id') != user_id:
                session_manager.revoke_session(session_id)
                raise AuthenticationError('Session validation failed.')

        return f(*args, **kwargs)
    return decorated


def require_permission(resource, action):
    """Decorator to enforce RBAC permission checks."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(g, 'roles') or not g.roles:
                raise AuthorizationError('Permissions required.')
            for role in g.roles:
                if rbac_manager.has_permission(role, resource, action):
                    return f(*args, **kwargs)
            raise AuthorizationError('Insufficient permissions.')
        return decorated
    return decorator
