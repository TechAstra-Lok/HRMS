import os
import secrets
from pathlib import Path
from dotenv import load_dotenv

from datetime import timedelta


load_dotenv(Path(__file__).resolve().parents[1] / '.env')


def _parse_token_timedelta(seconds_env: str, fallback_env: str, fallback_multiplier: int):
    value = os.getenv(seconds_env)
    if value:
        return timedelta(seconds=int(value))
    fallback = os.getenv(fallback_env)
    return timedelta(seconds=int(fallback) * fallback_multiplier) if fallback else timedelta(seconds=0)


class Settings:
    APP_NAME = os.getenv('APP_NAME', 'Enterprise HRMS')
    APP_ENV = os.getenv('APP_ENV', 'development')
    APP_DEBUG = os.getenv('APP_DEBUG', 'True').lower() == 'true'
    APP_URL = os.getenv('APP_URL', 'http://localhost:5000')
    SECRET_KEY = os.getenv('SECRET_KEY') or secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/hrms')
    SQLALCHEMY_POOL_SIZE = int(os.getenv('SQLALCHEMY_POOL_SIZE', '20'))
    SQLALCHEMY_MAX_OVERFLOW = int(os.getenv('SQLALCHEMY_MAX_OVERFLOW', '10'))
    SQLALCHEMY_POOL_TIMEOUT = int(os.getenv('SQLALCHEMY_POOL_TIMEOUT', '30'))
    SQLALCHEMY_POOL_RECYCLE = int(os.getenv('SQLALCHEMY_POOL_RECYCLE', '1800'))
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CORS_ORIGINS = [item.strip() for item in os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',') if item.strip()]
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_DEFAULT = os.getenv('RATE_LIMIT_DEFAULT', '100/hour')
    BCRYPT_ROUNDS = int(os.getenv('BCRYPT_ROUNDS', '12'))
    PASSWORD_MIN_LENGTH = int(os.getenv('PASSWORD_MIN_LENGTH', '12'))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or secrets.token_urlsafe(32)
    JWT_ACCESS_TOKEN_EXPIRES = _parse_token_timedelta('JWT_ACCESS_TOKEN_EXPIRES', 'JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 60)
    JWT_REFRESH_TOKEN_EXPIRES = _parse_token_timedelta('JWT_REFRESH_TOKEN_EXPIRES', 'JWT_REFRESH_TOKEN_EXPIRE_DAYS', 86400)
    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE', 'False') == 'True'
    CSRF_TOKEN = os.getenv('CSRF_TOKEN') or secrets.token_urlsafe(32)
    SESSION_IDLE_TIMEOUT_SECONDS = int(os.getenv('SESSION_IDLE_TIMEOUT_SECONDS', '1800'))
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY') or secrets.token_urlsafe(32)
    SECURITY_SALT = os.getenv('SECURITY_SALT') or secrets.token_urlsafe(16)


settings = Settings()
