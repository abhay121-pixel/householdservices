# config.py
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 2025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'noreply@householdservices.com'

    # Celery
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_TIMEZONE = 'UTC'
    
    # Celery Beat Schedule
    CELERYBEAT_SCHEDULE = {
        'daily-service-reminders': {
            'task': 'tasks.send_service_reminders',
            'schedule': timedelta(days=1),
            'args': (),
            'options': {'expires': 3600}
        },
        'monthly-activity-report': {
            'task': 'tasks.send_monthly_report',
            'schedule': timedelta(days=30),
            'args': (),
            'options': {'expires': 7200}
        }
    }
