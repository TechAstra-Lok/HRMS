from flask import g, request
from flask_restx import Namespace, Resource, fields
from ...core.security import require_auth, security_manager
from ...services.auth_service import AuthService
from ...exceptions import AuthenticationError, ValidationError

api = Namespace('auth', description='Authentication operations')
login_model = api.model('Login', {'email': fields.String(required=True), 'password': fields.String(required=True)})

@api.route('/login')
class LoginResource(Resource):
    def post(self):
        data = request.get_json() or {}
        service = AuthService()
        try:
            result = service.authenticate(data.get('email'), data.get('password'))
            return {'success': True, 'data': result}, 200
        except (AuthenticationError, ValidationError) as exc:
            return {'error': str(exc)}, 401

@api.route('/verify')
class VerifyResource(Resource):
    @require_auth
    def get(self):
        return {'success': True, 'data': {'user_id': g.user_id, 'tenant_id': g.tenant_id, 'roles': g.roles}}
