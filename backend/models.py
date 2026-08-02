"""Database models for Enterprise HRMS"""

from datetime import datetime, date
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, CheckConstraint, func
import uuid

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base model with common fields"""
    __abstract__ = True
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    
    def to_dict(self, exclude=[]):
        """Convert model to dictionary"""
        result = {}
        for column in self.__table__.columns:
            if column.name not in exclude:
                value = getattr(self, column.name)
                if isinstance(value, datetime):
                    value = value.isoformat()
                elif isinstance(value, date):
                    value = value.isoformat()
                elif isinstance(value, uuid.UUID):
                    value = str(value)
                result[column.name] = value
        return result


class Tenant(BaseModel):
    """Tenant model for multi-tenancy support"""
    __tablename__ = 'tenants'
    
    name = db.Column(db.String(200), nullable=False)
    subdomain = db.Column(db.String(100), unique=True, nullable=False, index=True)
    db_name = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(20), default='active', index=True)
    logo_url = db.Column(db.String(500))
    config = db.Column(JSONB, default={})
    
    # Relationships
    employees = db.relationship('Employee', backref='tenant', lazy='dynamic', cascade='all, delete-orphan')
    users = db.relationship('User', backref='tenant', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Tenant {self.name}>'


class User(BaseModel):
    """User model for authentication"""
    __tablename__ = 'users'
    
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_super_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    mfa_enabled = db.Column(db.Boolean, default=False)
    mfa_secret = db.Column(db.String(255))
    mfa_backup_codes = db.Column(db.Text)
    reset_token = db.Column(db.String(255))
    reset_token_expiry = db.Column(db.DateTime)
    preferences = db.Column(JSONB, default={})
    tenant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tenants.id'))
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Employee(BaseModel):
    """Employee model"""
    __tablename__ = 'employees'
    
    __table_args__ = (
        Index('idx_employee_tenant', 'tenant_id'),
        Index('idx_employee_status', 'status'),
        CheckConstraint('salary >= 0', name='check_salary_positive'),
    )
    
    # Personal Information
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(200))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    personal_email = db.Column(db.String(255))
    phone = db.Column(db.String(20), nullable=False)
    alternative_phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20))
    marital_status = db.Column(db.String(20))
    nationality = db.Column(db.String(50))
    
    # Address
    current_address = db.Column(db.Text)
    permanent_address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(50))
    postal_code = db.Column(db.String(20))
    
    # Employment
    employee_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    department = db.Column(db.String(100), index=True)
    designation = db.Column(db.String(100))
    reporting_manager_id = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id'))
    employment_type = db.Column(db.String(50), default='full_time')
    employment_status = db.Column(db.String(50), default='active', index=True)
    join_date = db.Column(db.Date, nullable=False)
    probation_end_date = db.Column(db.Date)
    confirmation_date = db.Column(db.Date)
    termination_date = db.Column(db.Date)
    termination_reason = db.Column(db.Text)
    
    # Compensation
    salary = db.Column(db.Float)
    salary_currency = db.Column(db.String(3), default='USD')
    pay_frequency = db.Column(db.String(20), default='monthly')
    hourly_rate = db.Column(db.Float)
    overtime_rate = db.Column(db.Float)
    
    # Benefits
    benefits = db.Column(JSONB, default={})
    benefit_eligibility_date = db.Column(db.Date)
    
    # Work
    work_location = db.Column(db.String(200))
    shift_start = db.Column(db.Time)
    shift_end = db.Column(db.Time)
    timezone = db.Column(db.String(50), default='UTC')
    
    # Documents
    documents = db.Column(JSONB, default={})
    profile_picture = db.Column(db.String(500))
    
    # Status
    status = db.Column(db.String(20), default='active', index=True)
    is_verified = db.Column(db.Boolean, default=False)
    verification_documents = db.Column(JSONB, default={})
    
    # Relationships
    tenant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tenants.id'), nullable=False)
    reporting_manager = db.relationship('Employee', remote_side='Employee.id')
    
    # System
    last_attendance_date = db.Column(db.Date)
    total_leaves = db.Column(db.Float, default=0)
    used_leaves = db.Column(db.Float, default=0)
    
    def __repr__(self):
        return f'<Employee {self.employee_id}: {self.first_name} {self.last_name}>'
    
    def get_full_name(self):
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return ' '.join(parts).strip()
    
    def get_display_name(self):
        return self.display_name or self.get_full_name()


class Attendance(BaseModel):
    """Attendance model"""
    __tablename__ = 'attendance'
    
    __table_args__ = (
        Index('idx_attendance_employee_date', 'employee_id', 'date'),
        Index('idx_attendance_tenant_date', 'tenant_id', 'date'),
    )
    
    employee_id = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    date_bs = db.Column(db.String(20))  # Nepali date
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    check_in_ip = db.Column(db.String(45))
    check_out_ip = db.Column(db.String(45))
    check_in_latitude = db.Column(db.Float)
    check_in_longitude = db.Column(db.Float)
    check_out_latitude = db.Column(db.Float)
    check_out_longitude = db.Column(db.Float)
    status = db.Column(db.String(20), default='present', index=True)
    total_hours = db.Column(db.Float, default=0)
    overtime_hours = db.Column(db.Float, default=0)
    break_hours = db.Column(db.Float, default=0)
    verification_method = db.Column(db.String(20))
    verification_status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)
    approved_by = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id'))
    approved_at = db.Column(db.DateTime)
    tenant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tenants.id'), nullable=False)
    
    def to_dict(self):
        data = super().to_dict()
        if data.get('check_in'):
            data['check_in'] = data['check_in'].isoformat() if isinstance(data['check_in'], datetime) else data['check_in']
        if data.get('check_out'):
            data['check_out'] = data['check_out'].isoformat() if isinstance(data['check_out'], datetime) else data['check_out']
        return data


class LeaveRequest(BaseModel):
    """Leave request model"""
    __tablename__ = 'leave_requests'
    
    employee_id = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_date_bs = db.Column(db.String(20))
    end_date_bs = db.Column(db.String(20))
    total_days = db.Column(db.Float, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending', index=True)
    approved_by = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id'))
    approved_at = db.Column(db.DateTime)
    rejection_reason = db.Column(db.Text)
    attachment_path = db.Column(db.String(500))
    tenant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tenants.id'), nullable=False)
    
    def to_dict(self):
        data = super().to_dict()
        for field in ['start_date', 'end_date', 'approved_at']:
            if data.get(field):
                data[field] = data[field].isoformat() if isinstance(data[field], (datetime, date)) else data[field]
        return data


class Payroll(BaseModel):
    """Payroll model"""
    __tablename__ = 'payroll'
    
    employee_id = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    basic_salary = db.Column(db.Float, nullable=False)
    allowances = db.Column(JSONB, default={})
    deductions = db.Column(JSONB, default={})
    bonuses = db.Column(JSONB, default={})
    total_allowances = db.Column(db.Float, default=0)
    total_deductions = db.Column(db.Float, default=0)
    total_bonuses = db.Column(db.Float, default=0)
    gross_pay = db.Column(db.Float, nullable=False)
    net_pay = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, default=0)
    payment_status = db.Column(db.String(20), default='pending', index=True)
    payment_date = db.Column(db.Date)
    payment_method = db.Column(db.String(50))
    notes = db.Column(db.Text)
    payslip_path = db.Column(db.String(500))
    tenant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tenants.id'), nullable=False)
    
    __table_args__ = (
        Index('idx_payroll_employee_month', 'employee_id', 'month', 'year'),
        Index('idx_payroll_tenant', 'tenant_id'),
    )


class BiometricDevice(BaseModel):
    """Biometric device model"""
    __tablename__ = 'biometric_devices'
    
    name = db.Column(db.String(100), nullable=False)
    device_id = db.Column(db.String(50), unique=True, nullable=False)
    device_type = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    model = db.Column(db.String(50))
    ip_address = db.Column(db.String(45), nullable=False)
    port = db.Column(db.Integer, default=4370)
    api_key = db.Column(db.String(255))
    api_secret = db.Column(db.String(255))
    serial_number = db.Column(db.String(50))
    firmware_version = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='online')
    last_sync_time = db.Column(db.DateTime)
    sync_frequency = db.Column(db.Integer, default=300)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location_name = db.Column(db.String(200))
    config = db.Column(JSONB, default={})
    tenant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tenants.id'), nullable=False)


class AuditLog(BaseModel):
    """Audit log model"""
    __tablename__ = 'audit_logs'
    
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    tenant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tenants.id'))
    action = db.Column(db.String(100), nullable=False, index=True)
    resource_type = db.Column(db.String(50))
    resource_id = db.Column(db.String(50))
    details = db.Column(JSONB, default={})
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    status = db.Column(db.String(20), default='success')
    
    __table_args__ = (
        Index('idx_audit_user', 'user_id'),
        Index('idx_audit_tenant', 'tenant_id'),
        Index('idx_audit_action', 'action'),
        Index('idx_audit_timestamp', 'created_at'),
    )


class Notification(BaseModel):
    """Notification model"""
    __tablename__ = 'notifications'
    
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    tenant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tenants.id'))
    type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    data = db.Column(JSONB, default={})
    is_read = db.Column(db.Boolean, default=False, index=True)
    read_at = db.Column(db.DateTime)
    priority = db.Column(db.String(20), default='normal')
    channel = db.Column(db.String(20), default='in_app')
    external_id = db.Column(db.String(255))
    sent_at = db.Column(db.DateTime)
    
    __table_args__ = (
        Index('idx_notification_user', 'user_id'),
        Index('idx_notification_read', 'is_read'),
    )


class PerformanceReview(BaseModel):
    """Performance review model"""
    __tablename__ = 'performance_reviews'
    
    employee_id = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id'), nullable=False)
    reviewer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id'), nullable=False)
    review_period_start = db.Column(db.Date, nullable=False)
    review_period_end = db.Column(db.Date, nullable=False)
    review_date = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Float)
    strengths = db.Column(db.Text)
    weaknesses = db.Column(db.Text)
    achievements = db.Column(db.Text)
    goals = db.Column(db.Text)
    feedback = db.Column(db.Text)
    status = db.Column(db.String(20), default='draft')
    is_self_review = db.Column(db.Boolean, default=False)
    rating_scale = db.Column(db.String(20), default='1-5')
    areas_for_improvement = db.Column(db.Text)
    next_review_date = db.Column(db.Date)
    tenant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tenants.id'), nullable=False)


class Goal(BaseModel):
    """Goals/OKR model"""
    __tablename__ = 'goals'
    
    employee_id = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50))  # OKR, KPI, Personal
    priority = db.Column(db.String(20), default='medium')
    status = db.Column(db.String(20), default='not_started')
    progress = db.Column(db.Float, default=0)
    start_date = db.Column(db.Date)
    target_date = db.Column(db.Date)
    completion_date = db.Column(db.Date)
    parent_goal_id = db.Column(UUID(as_uuid=True), db.ForeignKey('goals.id'))
    key_results = db.Column(JSONB, default=[])
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id'))
    tenant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tenants.id'), nullable=False)
