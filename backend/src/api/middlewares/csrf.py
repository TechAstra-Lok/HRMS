from functools import wraps
from flask import request, jsonify, current_app


def validate_csrf_token(token: str) -> bool:
    expected = current_app.config.get('CSRF_TOKEN')
    return bool(token and expected and token == expected)


def csrf_protect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method not in ('GET', 'HEAD', 'OPTIONS'):
            token = request.headers.get('X-CSRF-Token') or request.cookies.get('csrf_token')
            if not token or not validate_csrf_token(token):
                return jsonify({'error': 'csrf_validation_failed', 'message': 'Invalid CSRF token.'}), 403
        return f(*args, **kwargs)
    return decorated_function
