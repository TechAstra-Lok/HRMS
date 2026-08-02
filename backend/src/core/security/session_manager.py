"""In-memory session storage for local development."""

import os
from datetime import datetime
from typing import Optional


class SessionManager:
    """Manage lightweight user session metadata without Redis."""

    def __init__(self, redis_url: Optional[str] = None):
        self.redis_url = redis_url or os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.timeout = int(os.getenv('SESSION_IDLE_TIMEOUT_SECONDS', '1800'))
        self._sessions = {}

    def create_session(self, session_id: str, user_id: str, tenant_id: str, roles: list) -> None:
        payload = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'roles': ','.join(roles),
            'created_at': datetime.utcnow().isoformat(),
        }
        self._sessions[session_id] = payload

    def validate_session(self, session_id: str) -> Optional[dict]:
        if not session_id:
            return None
        session_data = self._sessions.get(session_id)
        if not session_data:
            return None
        return {
            'user_id': session_data.get('user_id'),
            'tenant_id': session_data.get('tenant_id'),
            'roles': session_data.get('roles', '').split(',') if session_data.get('roles') else [],
        }

    def revoke_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)


session_manager = SessionManager()
