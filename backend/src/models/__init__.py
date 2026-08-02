"""Lightweight model shim for local startup."""

from datetime import date, datetime

from flask_sqlalchemy import SQLAlchemy


class _BaseModel(object):
    """Minimal base class used by the local compatibility layer."""

    def to_dict(self):
        return {}


db = SQLAlchemy()


class _QuerySet(list):
    def filter_by(self, **kwargs):
        items = list(self)
        for key, value in kwargs.items():
            items = [item for item in items if getattr(item, key, None) == value]
        return _QuerySet(items)

    def count(self):
        return len(self)

    def all(self):
        return list(self)

    def first(self):
        return self[0] if self else None


class _ModelRegistry:
    _instances = {}

    @classmethod
    def get(cls, model_name):
        if model_name not in cls._instances:
            cls._instances[model_name] = []
        return cls._instances[model_name]


class _LocalModel(_BaseModel):
    _registry_name = None

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)
        if self._registry_name:
            _ModelRegistry.get(self._registry_name).append(self)

    def to_dict(self):
        data = dict(self.__dict__)
        data.pop('_sa_instance_state', None)
        return data

    @classmethod
    def query(cls):
        return _QuerySet(_ModelRegistry.get(cls._registry_name or cls.__name__.lower()))


class User(_LocalModel):
    _registry_name = 'users'

    def __init__(self, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_deleted', False)
        kwargs.setdefault('is_super_admin', False)
        kwargs.setdefault('password_hash', '')
        super().__init__(**kwargs)


class Tenant(_LocalModel):
    _registry_name = 'tenants'


class Employee(_LocalModel):
    _registry_name = 'employees'

    def __init__(self, **kwargs):
        kwargs.setdefault('is_deleted', False)
        kwargs.setdefault('email', '')
        kwargs.setdefault('first_name', '')
        kwargs.setdefault('last_name', '')
        kwargs.setdefault('department', 'Operations')
        kwargs.setdefault('designation', 'Employee')
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'department': getattr(self, 'department', 'Operations'),
            'designation': getattr(self, 'designation', 'Employee'),
            'phone': getattr(self, 'phone', ''),
            'employee_id': getattr(self, 'employee_id', ''),
            'tenant_id': getattr(self, 'tenant_id', None),
        }


class Attendance(_LocalModel):
    _registry_name = 'attendances'

    def __init__(self, **kwargs):
        kwargs.setdefault('status', 'present')
        super().__init__(**kwargs)


class LeaveRequest(_LocalModel):
    _registry_name = 'leave_requests'

    def __init__(self, **kwargs):
        kwargs.setdefault('status', 'pending')
        super().__init__(**kwargs)


class AuditLog(_LocalModel):
    _registry_name = 'audit_logs'

    def __init__(self, **kwargs):
        kwargs.setdefault('details', {})
        kwargs.setdefault('status', 'success')
        super().__init__(**kwargs)


if not _ModelRegistry.get('employees'):
    Employee(id='emp-001', first_name='Asha', last_name='Patel', email='asha@hrms.local', department='Engineering', designation='Engineer', tenant_id='demo-tenant')
    Employee(id='emp-002', first_name='Mina', last_name='Chen', email='mina@hrms.local', department='HR', designation='HR Manager', tenant_id='demo-tenant')
    Employee(id='emp-003', first_name='Derek', last_name='Morris', email='derek@hrms.local', department='Finance', designation='Analyst', tenant_id='demo-tenant')

if not _ModelRegistry.get('attendances'):
    Attendance(id='att-001', employee_id='emp-001', date=date.today(), check_in=datetime.utcnow(), status='present', tenant_id='demo-tenant')
    Attendance(id='att-002', employee_id='emp-002', date=date.today(), check_in=datetime.utcnow(), status='present', tenant_id='demo-tenant')

if not _ModelRegistry.get('leave_requests'):
    LeaveRequest(id='leave-001', employee_id='emp-001', status='pending', tenant_id='demo-tenant')


__all__ = ['db', 'User', 'Tenant', 'Employee', 'Attendance', 'LeaveRequest', 'AuditLog']
