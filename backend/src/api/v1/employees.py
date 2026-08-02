from flask import g, request
from flask_restx import Namespace, Resource, fields
from ...core.security import require_auth, require_permission
from ...services.employee_service import EmployeeService

api = Namespace('employees', description='Employee management')
employee_model = api.model('Employee', {'first_name': fields.String(required=True), 'last_name': fields.String(required=True), 'email': fields.String(required=True)})

@api.route('/')
class EmployeeListResource(Resource):
    @require_auth
    def get(self):
        return {'success': True, 'data': EmployeeService.get_employees(g.tenant_id)}

    @require_auth
    @require_permission('employee', 'create')
    @api.expect(employee_model)
    def post(self):
        data = request.get_json() or {}
        data['tenant_id'] = g.tenant_id
        employee = EmployeeService.create_employee(data)
        return {'success': True, 'data': employee.to_dict()}, 201
