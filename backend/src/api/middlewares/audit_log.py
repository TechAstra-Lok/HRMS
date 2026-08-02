from functools import wraps
from flask import request, g, current_app
from src.models import AuditLog, db


def register_audit_logging(app):
    @app.after_request
    def audit_response(response):
        if request.method not in ('GET', 'HEAD', 'OPTIONS') and response.status_code < 500:
            try:
                audit = AuditLog(
                    user_id=getattr(g, 'user_id', None),
                    tenant_id=getattr(g, 'tenant_id', None),
                    action=f'{request.method} {request.path}',
                    resource_type=request.endpoint or 'api',
                    resource_id=request.view_args.get('id') if request.view_args else None,
                    details={
                        'query': request.args.to_dict(flat=True),
                        'status_code': response.status_code,
                    },
                    ip_address=request.headers.get('X-Forwarded-For', request.remote_addr),
                    user_agent=request.headers.get('User-Agent'),
                    status='success'
                )
                db.session.add(audit)
                db.session.commit()
            except Exception:
                db.session.rollback()
        return response


def audit_action(action: str, resource_type: str = None, resource_id: str = None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = f(*args, **kwargs)
            try:
                audit = AuditLog(
                    user_id=getattr(g, 'user_id', None),
                    tenant_id=getattr(g, 'tenant_id', None),
                    action=action,
                    resource_type=resource_type,
                    resource_id=resource_id,
                    details={
                        'path': request.path,
                        'method': request.method,
                        'query': request.args.to_dict(flat=True),
                    },
                    ip_address=request.headers.get('X-Forwarded-For', request.remote_addr),
                    user_agent=request.headers.get('User-Agent'),
                    status='success'
                )
                db.session.add(audit)
                db.session.commit()
            except Exception:
                db.session.rollback()
            return response
        return decorated_function
    return decorator
