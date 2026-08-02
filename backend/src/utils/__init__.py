"""Utility functions and helpers"""

import uuid
from datetime import datetime, date, timedelta
from typing import Any, Dict

def generate_id():
    """Generate unique ID"""
    return str(uuid.uuid4())

def get_today():
    """Get today's date"""
    return date.today()

def get_current_timestamp():
    """Get current timestamp"""
    return datetime.utcnow()

def parse_date(date_string: str) -> date:
    """Parse date string"""
    if isinstance(date_string, date):
        return date_string
    return datetime.strptime(date_string, '%Y-%m-%d').date()

def parse_datetime(datetime_string: str) -> datetime:
    """Parse datetime string"""
    if isinstance(datetime_string, datetime):
        return datetime_string
    return datetime.fromisoformat(datetime_string)

def calculate_days(start_date: date, end_date: date) -> float:
    """Calculate number of days between dates"""
    delta = end_date - start_date
    return delta.days + 1

def get_month_year():
    """Get current month and year"""
    now = datetime.utcnow()
    return now.month, now.year

def format_date(date_obj: date) -> str:
    """Format date to string"""
    return date_obj.strftime('%Y-%m-%d')

def format_datetime(datetime_obj: datetime) -> str:
    """Format datetime to ISO format"""
    return datetime_obj.isoformat()

def dict_to_camel_case(snake_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Convert dict keys from snake_case to camelCase"""
    result = {}
    for key, value in snake_dict.items():
        camel_case_key = ''.join(
            x.capitalize() if i > 0 else x 
            for i, x in enumerate(key.split('_'))
        )
        result[camel_case_key] = value
    return result
