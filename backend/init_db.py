"""Database initialization script"""

import logging
import os
import secrets
from pathlib import Path
from dotenv import load_dotenv
from app import create_app
from models import db, Tenant, User
from src.core.security import hash_manager
import uuid

load_dotenv(Path(__file__).resolve().parent / '.env')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def init_db():
    """Initialize database with sample data"""
    
    app = create_app()
    
    if app.config.get('APP_ENV') == 'production':
        raise RuntimeError('init_db.py must not be run in production')

    with app.app_context():
        # Drop all tables in non-production environments only
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create default tenant
        tenant = Tenant(
            id=uuid.uuid4(),
            name='Default Company',
            subdomain='default',
            db_name='hrms_default',
            status='active'
        )
        
        db.session.add(tenant)
        db.session.commit()
        
        # Create admin user from environment variables or generate a secure password
        admin_email = os.getenv('ADMIN_EMAIL')
        if not admin_email or admin_email.strip().startswith('<'):
            raise RuntimeError(
                'ADMIN_EMAIL must be set in environment or backend/.env before running init_db.py'
            )

        admin_password = os.getenv('ADMIN_PASSWORD')
        if not admin_password or admin_password.strip().startswith('<'):
            admin_password = secrets.token_urlsafe(24)

        admin_user = User(
            id=uuid.uuid4(),
            email=admin_email,
            password_hash=hash_manager.hash_password(admin_password),
            first_name='Admin',
            last_name='User',
            is_active=True,
            is_super_admin=True,
            tenant_id=tenant.id
        )

        db.session.add(admin_user)
        db.session.commit()
        
        logger.info("Database initialization completed.")
        logger.info("Admin user created for %s", admin_user.email)
        if not os.getenv('ADMIN_PASSWORD') or os.getenv('ADMIN_PASSWORD').strip().startswith('<'):
            logger.warning("ADMIN_PASSWORD was not set or was a placeholder. Generated admin password: %s", admin_password)

if __name__ == '__main__':
    init_db()
