"""Exceptions module"""


class HRMSException(Exception):
    """Base exception for HRMS."""


class AuthenticationException(HRMSException):
    """Authentication failed."""


class AuthorizationException(HRMSException):
    """User not authorized."""


class ValidationException(HRMSException):
    """Validation failed."""


class ResourceNotFoundException(HRMSException):
    """Resource not found."""


class ConflictException(HRMSException):
    """Resource conflict."""


class RateLimitException(HRMSException):
    """Rate limit exceeded."""


AuthenticationError = AuthenticationException
AuthorizationError = AuthorizationException
ValidationError = ValidationException
NotFoundError = ResourceNotFoundException
BusinessError = ConflictException
