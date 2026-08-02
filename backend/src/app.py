from datetime import timedelta

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_socketio import SocketIO

from .config import settings
from .api.middlewares import apply_security_headers, register_error_handlers, register_audit_logging
from .api.v1 import auth_bp, employees_bp, attendance_bp, leaves_bp, payroll_bp, dashboard_bp
from .models import db


def create_app():
    app = Flask(__name__, static_folder='public', static_url_path='')
    app.config.update(
        APP_ENV=settings.APP_ENV,
        SECRET_KEY=settings.SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=settings.SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_TYPE='redis',
        SESSION_PERMANENT=False,
        SESSION_USE_SIGNER=True,
        SESSION_REFRESH_EACH_REQUEST=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=settings.SESSION_COOKIE_SECURE,
        SESSION_COOKIE_SAMESITE='Lax',
        JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
        JWT_ACCESS_TOKEN_EXPIRES=settings.JWT_ACCESS_TOKEN_EXPIRES,
        JWT_REFRESH_TOKEN_EXPIRES=settings.JWT_REFRESH_TOKEN_EXPIRES,
        CSRF_TOKEN=settings.CSRF_TOKEN,
        RATELIMIT_HEADERS_ENABLED=True,
        CACHE_TYPE='redis',
        CACHE_REDIS_URL=settings.REDIS_URL,
        CACHE_KEY_PREFIX='hrms_',
        JSON_SORT_KEYS=False,
        JSONIFY_PRETTYPRINT_REGULAR=False,
        PREFERRED_URL_SCHEME='https' if settings.APP_ENV == 'production' else 'http',
    )

    CORS(app, origins=settings.CORS_ORIGINS, supports_credentials=True)
    db.init_app(app)
    Migrate(app, db)
    Cache(app)
    Limiter(app, key_func=get_remote_address, default_limits=[settings.RATE_LIMIT_DEFAULT])
    SocketIO(app, cors_allowed_origins=settings.CORS_ORIGINS, async_mode='eventlet')

    app.after_request(apply_security_headers)
    register_audit_logging(app)
    register_error_handlers(app)

    @app.before_request
    def enforce_csrf():
        if request.method not in ('GET', 'HEAD', 'OPTIONS'):
            exempt_paths = ['/health', '/api/v1/auth/login', '/api/v1/auth/refresh']
            if request.path not in exempt_paths:
                token = request.headers.get('X-CSRF-Token') or request.cookies.get('csrf_token')
                if not token or token != app.config.get('CSRF_TOKEN'):
                    return jsonify({'error': 'csrf_validation_failed', 'message': 'Invalid CSRF token.'}), 403

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(employees_bp, url_prefix='/api/v1/employees')
    app.register_blueprint(attendance_bp, url_prefix='/api/v1/attendance')
    app.register_blueprint(leaves_bp, url_prefix='/api/v1/leaves')
    app.register_blueprint(payroll_bp, url_prefix='/api/v1/payroll')
    app.register_blueprint(dashboard_bp, url_prefix='/api/v1/dashboard')

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy'})

    return app


app = create_app()
