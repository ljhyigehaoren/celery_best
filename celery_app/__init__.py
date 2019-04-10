from celery import Celery

app = Celery(
    'celeryApp',
    include=[
        'celery_app.teskone',
        'celery_app.tesktwo',
    ]
)
app.config_from_object('celery_app.celeryconf')