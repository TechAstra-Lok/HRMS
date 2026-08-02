from flask import g, request
from flask_restx import Namespace, Resource
from ...core.security import require_auth, require_permission
from ...services.payroll_service import PayrollService

api = Namespace('payroll', description='Payroll operations')

@api.route('/calculate')
class PayrollResource(Resource):
    @require_auth
    @require_permission('payroll', 'process')
    def post(self):
        data = request.get_json() or {}
        result = PayrollService.calculate_payroll(g.tenant_id, data)
        return {'success': True, 'data': result}
