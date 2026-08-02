from flask import g
from flask_restx import Namespace, Resource
from ...core.security import require_auth
from ...services.dashboard_service import DashboardService

api = Namespace('dashboard', description='Dashboard operations')

@api.route('/stats')
class DashboardStatsResource(Resource):
    @require_auth
    def get(self):
        return {'success': True, 'data': DashboardService.get_stats(g.tenant_id)}
