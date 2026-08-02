"""JWT token management utilities"""

import jwt
import uuid
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import os

class JWTManager:
    """Manage JWT tokens"""
    
    SECRET_KEY = os.getenv('JWT_SECRET_KEY') or secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 604800))
    ALGORITHM = 'HS256'
    
    @staticmethod
    def generate_access_token(user_id: str, tenant_id: str = None, 
                             roles: list = None) -> str:
        """Generate access token"""
        payload = {
            'sub': user_id,
            'tenant': tenant_id,
            'roles': roles or ['employee'],
            'jti': str(uuid.uuid4()),
            'type': 'access',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=JWTManager.ACCESS_TOKEN_EXPIRES)
        }
        return jwt.encode(payload, JWTManager.SECRET_KEY, algorithm=JWTManager.ALGORITHM)
    
    @staticmethod
    def generate_refresh_token(user_id: str) -> str:
        """Generate refresh token"""
        payload = {
            'sub': user_id,
            'jti': str(uuid.uuid4()),
            'type': 'refresh',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=JWTManager.REFRESH_TOKEN_EXPIRES)
        }
        return jwt.encode(payload, JWTManager.SECRET_KEY, algorithm=JWTManager.ALGORITHM)
    
    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """Verify and decode token"""
        try:
            return jwt.decode(token, JWTManager.SECRET_KEY, algorithms=[JWTManager.ALGORITHM], options={
                'require_exp': True,
                'verify_aud': False,
                'verify_iss': False,
            })
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
    
    @staticmethod
    def get_user_id_from_token(token: str) -> Optional[str]:
        """Extract user ID from token"""
        try:
            payload = JWTManager.verify_token(token)
            return payload.get('sub')
        except Exception:
            return None


# Global instance
jwt_manager = JWTManager()
