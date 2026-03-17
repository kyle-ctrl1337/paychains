import os
from celery import Celery
from celery.schedules import crontab

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "paychains",
    broker=redis_url,
    backend=redis_url,
    include=[
        "app.workers.webhook_tasks",
        "app.workers.subscription_tasks",
        "app.workers.monitor_tasks",
        "app.workers.conversion_tasks",
        "app.workers.payout_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

# Beat schedule for recurring tasks
celery_app.conf.beat_schedule = {
    "check-due-subscriptions": {
        "task": "app.workers.subscription_tasks.check_due_subscriptions",
        "schedule": 300.0,  # every 5 minutes
    },
    "expire-pending-payments": {
        "task": "app.workers.monitor_tasks.expire_pending_payments",
        "schedule": 60.0,  # every minute
    },
    "retry-failed-webhooks": {
        "task": "app.workers.webhook_tasks.retry_failed_webhooks",
        "schedule": 60.0,  # every minute
    },
    "poll-pending-payments": {
        "task": "app.workers.monitor_tasks.poll_pending_payments",
        "schedule": 15.0,  # every 15 seconds
    },
}
