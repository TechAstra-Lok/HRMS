from flask import g, request
from flask_restx import Namespace, Resource
from ...core.security import require_auth
from ...services.attendance_service import AttendanceService

api = Namespace('attendance', description='Attendance management')

@api.route('/check-in')
class CheckInResource(Resource):
    @require_auth
    def post(self):
        data = request.get_json() or {}
        result = AttendanceService.check_in(g.user_id, g.tenant_id, data)
        return {'success': True, 'data': result}

@api.route('/check-out')
class CheckOutResource(Resource):
    @require_auth
    def post(self):
        data = request.get_json() or {}
        result = AttendanceService.check_out(g.user_id, g.tenant_id, data)
        return {'success': True, 'data': result}
