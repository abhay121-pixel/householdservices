from celery import Celery
from .celery_config import BROKER_URL, BACKEND_URL

app = Celery(
    'backend',
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=['backend.tasks']  # Add your task modules here
)

# Import celery config
app.config_from_object('backend.celery_config')

if __name__ == '__main__':
    app.start() 