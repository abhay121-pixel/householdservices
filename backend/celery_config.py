from celery import Celery
from celery.schedules import crontab

# Make the broker URL more explicit
BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6379/0'

celery = Celery(
    'tasks',  # Change this to a more specific name for your application
    broker=BROKER_URL,
    backend=BACKEND_URL
)

# Optional: Add some additional configurations
celery.conf.update(
    broker_connection_retry_on_startup=True,
    result_backend=BACKEND_URL
)

CELERY_BEAT_SCHEDULE = {
    'generate-monthly-report': {
        'task': 'tasks.generate_monthly_report',
        'schedule': 10.0,
    },
}
celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE
