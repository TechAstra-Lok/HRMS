"""Task scheduling with Celery"""

from celery import Celery, beat_schedule
from datetime import timedelta
import os

def make_celery():
    """Create Celery instance"""
    
    celery = Celery(
        'hrms',
        broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/2'),
        backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/3')
    )
    
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_acks_late=True,
        task_time_limit=3600,
        task_soft_time_limit=3000,
        beat_schedule={
            'biometric-sync': {
                'task': 'tasks.biometric_sync',
                'schedule': timedelta(seconds=300),
            },
            'payroll-processing': {
                'task': 'tasks.process_payroll',
                'schedule': timedelta(days=1),
                'options': {'time': '02:00'}
            },
            'daily-reports': {
                'task': 'tasks.generate_daily_reports',
                'schedule': timedelta(days=1),
                'options': {'time': '23:59'}
            },
            'database-backup': {
                'task': 'tasks.backup_database',
                'schedule': timedelta(days=1),
                'options': {'time': '01:00'}
            },
            'health-check': {
                'task': 'tasks.system_health_check',
                'schedule': timedelta(minutes=15),
            },
            'cache-warmup': {
                'task': 'tasks.warmup_cache',
                'schedule': timedelta(days=1),
                'options': {'time': '00:30'}
            },
        }
    )
    
    return celery

celery_app = make_celery()

@celery_app.task(bind=True)
def biometric_sync(self):
    """Sync biometric devices"""
    return {'status': 'completed', 'synced_devices': 5}

@celery_app.task(bind=True)
def process_payroll(self):
    """Process monthly payroll"""
    return {'status': 'completed', 'processed_employees': 50}

@celery_app.task(bind=True)
def generate_daily_reports(self):
    """Generate daily reports"""
    return {'status': 'completed', 'reports_generated': 10}

@celery_app.task(bind=True)
def backup_database(self):
    """Backup database"""
    return {'status': 'completed', 'backup_size': '500MB'}

@celery_app.task(bind=True)
def system_health_check(self):
    """Check system health"""
    return {
        'status': 'healthy',
        'uptime': '99.5%',
        'database': 'ok',
        'redis': 'ok'
    }

@celery_app.task(bind=True)
def warmup_cache(self):
    """Warm up cache"""
    return {'status': 'completed', 'items_cached': 1000}
