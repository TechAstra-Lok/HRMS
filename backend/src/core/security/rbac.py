"""Role-Based Access Control (RBAC) utilities"""

from typing import List, Dict, Any
from ..constants import UserRole, Permission

class RBACManager:
    """Role-Based Access Control Manager"""
    
    def __init__(self):
        self.role_permissions = self._init_permissions()
    
    def _init_permissions(self) -> Dict[str, List[str]]:
        """Initialize role permissions mapping"""
        return {
            UserRole.SUPER_ADMIN.value: ['*'],
            
            UserRole.TENANT_ADMIN.value: [
                Permission.EMPLOYEE_MANAGE.value,
                Permission.ATTENDANCE_MANAGE.value,
                Permission.PAYROLL_MANAGE.value,
                Permission.RECRUITMENT_MANAGE.value,
                Permission.PERFORMANCE_MANAGE.value,
                Permission.REPORTS_MANAGE.value,
                Permission.SETTINGS_MANAGE.value,
                Permission.TENANT_READ.value,
            ],
            
            UserRole.HR_MANAGER.value: [
                Permission.EMPLOYEE_READ.value,
                Permission.EMPLOYEE_CREATE.value,
                Permission.EMPLOYEE_UPDATE.value,
                Permission.ATTENDANCE_READ.value,
                Permission.ATTENDANCE_APPROVE.value,
                Permission.PAYROLL_READ.value,
                Permission.PAYROLL_PROCESS.value,
                Permission.RECRUITMENT_READ.value,
                Permission.RECRUITMENT_CREATE.value,
                Permission.PERFORMANCE_READ.value,
                Permission.PERFORMANCE_REVIEW.value,
                Permission.REPORTS_READ.value,
            ],
            
            UserRole.DEPARTMENT_MANAGER.value: [
                Permission.EMPLOYEE_READ.value,
                Permission.ATTENDANCE_READ.value,
                Permission.ATTENDANCE_VIEW_TEAM.value,
                Permission.LEAVE_APPROVE.value,
                Permission.PERFORMANCE_READ.value,
                Permission.PERFORMANCE_REVIEW.value,
                Permission.REPORTS_READ.value,
            ],
            
            UserRole.EMPLOYEE.value: [
                Permission.EMPLOYEE_READ.value,
                Permission.ATTENDANCE_READ.value,
                Permission.LEAVE_APPLY.value,
                Permission.LEAVE_READ.value,
                Permission.PAYROLL_READ.value,
                Permission.PERFORMANCE_READ.value,
            ]
        }
    
    def has_permission(self, role: str, resource: str, action: str) -> bool:
        """Check if role has permission for resource action"""
        if role not in self.role_permissions:
            return False
        
        permissions = self.role_permissions[role]
        required = f"{resource}:{action}"
        
        for perm in permissions:
            if perm == '*':
                return True
            if perm == required:
                return True
            if perm.endswith(':*'):
                if required.startswith(perm.replace(':*', ':')):
                    return True
        return False
    
    def get_permissions(self, role: str) -> List[str]:
        """Get all permissions for a role"""
        return self.role_permissions.get(role, [])
    
    def has_any_permission(self, role: str, resources: List[tuple]) -> bool:
        """Check if role has any of the given permissions"""
        for resource, action in resources:
            if self.has_permission(role, resource, action):
                return True
        return False


# Global instance
rbac_manager = RBACManager()
