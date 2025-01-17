from celery import Celery
from celery_worker import tasks 


app = Celery(__name__)

app.conf.broker_url = "redis://redis:6379/0"
app.conf.result_backend = "redis://redis:6379/0"
app.conf.task_serializer = "json"
# app.config_from_object('celery_worker.celery_app')
# app.autodiscover_tasks(["celery_worker.tasks"])
