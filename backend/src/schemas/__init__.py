"""Schemas for request/response validation"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class CreateEmployeeRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    department: str
    designation: str
    date_of_birth: date
    join_date: date

class ApplyLeaveRequest(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    total_days: float
    reason: str

class AttendanceCheckInRequest(BaseModel):
    employee_id: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    is_active: bool

class EmployeeResponse(BaseModel):
    id: str
    employee_id: str
    first_name: str
    last_name: str
    email: str
    department: str
    designation: str
    status: str

class AttendanceResponse(BaseModel):
    id: str
    employee_id: str
    date: date
    check_in: Optional[datetime]
    check_out: Optional[datetime]
    status: str
    total_hours: float
