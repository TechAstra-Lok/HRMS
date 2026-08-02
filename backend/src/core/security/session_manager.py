"""Redis-backed session and token management."""

import os
import redis
from datetime import datetime, timedelta
from typing import Optional


class SessionManager:
    """Manage Redis-backed user session metadata."""

    def __init__(self, redis_url: Optional[str] = None):
        self.redis_url = redis_url or os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.timeout = int(os.getenv('SESSION_IDLE_TIMEOUT_SECONDS', '1800'))
        self.redis = redis.Redis.from_url(self.redis_url, decode_responses=True)

    def create_session(self, session_id: str, user_id: str, tenant_id: str, roles: list) -> None:
        payload = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'roles': ','.join(roles),
            'created_at': datetime.utcnow().isoformat(),
        }
        self.redis.hset(f'session:{session_id}', mapping=payload)
        self.redis.expire(f'session:{session_id}', self.timeout)

    def validate_session(self, session_id: str) -> Optional[dict]:
        if not session_id:
            return None
        key = f'session:{session_id}'
        if not self.redis.exists(key):
            return None
        self.redis.expire(key, self.timeout)
        session_data = self.redis.hgetall(key)
        if not session_data:
            return None
        return {
            'user_id': session_data.get('user_id'),
            'tenant_id': session_data.get('tenant_id'),
            'roles': session_data.get('roles', '').split(',') if session_data.get('roles') else [],
        }

    def revoke_session(self, session_id: str) -> None:
        self.redis.delete(f'session:{session_id}')


session_manager = SessionManager()
