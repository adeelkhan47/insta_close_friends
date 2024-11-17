from datetime import timedelta

from config import settings

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

broker_url = settings.CELERY_BROKER_REDIS
broker_transport_options = {"visibility_timeout": 3600 * 6}
result_backend = settings.CELERY_BROKER_REDIS
result_persistent = False

imports = ("tasks.email")


beat_schedule = {
    "account_processed": {
        "task": "tasks.email.process_new",
        "schedule": timedelta(seconds=1)
    }
}




