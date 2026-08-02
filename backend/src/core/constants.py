"""Constants and enums"""

from enum import Enum

class UserRole(str, Enum):
    """User roles"""
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin"
    HR_MANAGER = "hr_manager"
    DEPARTMENT_MANAGER = "department_manager"
    EMPLOYEE = "employee"


class Permission(str, Enum):
    """Permissions"""
    EMPLOYEE_READ = "employee:read"
    EMPLOYEE_CREATE = "employee:create"
    EMPLOYEE_UPDATE = "employee:update"
    EMPLOYEE_DELETE = "employee:delete"
    EMPLOYEE_MANAGE = "employee:manage"
    
    ATTENDANCE_READ = "attendance:read"
    ATTENDANCE_VIEW_TEAM = "attendance:view_team"
    ATTENDANCE_MANAGE = "attendance:manage"
    ATTENDANCE_APPROVE = "attendance:approve"
    
    LEAVE_READ = "leave:read"
    LEAVE_APPLY = "leave:apply"
    LEAVE_APPROVE = "leave:approve"
    LEAVE_MANAGE = "leave:manage"
    
    PAYROLL_READ = "payroll:read"
    PAYROLL_PROCESS = "payroll:process"
    PAYROLL_MANAGE = "payroll:manage"
    
    RECRUITMENT_READ = "recruitment:read"
    RECRUITMENT_CREATE = "recruitment:create"
    RECRUITMENT_MANAGE = "recruitment:manage"
    
    PERFORMANCE_READ = "performance:read"
    PERFORMANCE_REVIEW = "performance:review"
    PERFORMANCE_MANAGE = "performance:manage"
    
    REPORTS_READ = "reports:read"
    REPORTS_MANAGE = "reports:manage"
    
    SETTINGS_MANAGE = "settings:manage"
    TENANT_READ = "tenant:read"


class AttendanceStatus(str, Enum):
    """Attendance status"""
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    LEAVE = "leave"
    WORK_FROM_HOME = "work_from_home"


class LeaveType(str, Enum):
    """Leave types"""
    SICK = "sick"
    CASUAL = "casual"
    EARNED = "earned"
    UNPAID = "unpaid"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    BEREAVEMENT = "bereavement"


class LeaveStatus(str, Enum):
    """Leave request status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class EmploymentStatus(str, Enum):
    """Employment status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROBATION = "probation"
    RESIGNED = "resigned"
    TERMINATED = "terminated"
    SUSPENDED = "suspended"


class NotificationType(str, Enum):
    """Notification types"""
    ATTENDANCE = "attendance"
    LEAVE = "leave"
    PAYROLL = "payroll"
    SYSTEM = "system"
    ALERT = "alert"
    INFO = "info"


class VerificationStatus(str, Enum):
    """Document verification status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
