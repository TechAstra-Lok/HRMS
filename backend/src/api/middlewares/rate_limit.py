from flask import request, jsonify
from functools import wraps
from src.core.security import rate_limiter


def rate_limit(limit: str = None):
    """Rate limiting decorator using Redis-backed rate limiter."""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            key = request.remote_addr or request.headers.get('X-Forwarded-For', 'unknown')
            allowed, remaining, reset = rate_limiter.is_allowed(key, limit)
            if not allowed:
                response = jsonify({'error': 'rate_limit_exceeded', 'message': 'Too many requests, try again later.'})
                response.headers['Retry-After'] = str(reset)
                return response, 429
            return f(*args, **kwargs)
        return wrapped
    return decorator
