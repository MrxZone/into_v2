#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from kombu import Queue
from celery import Celery

celery_app = Celery(
    'celery_app',
    backend=os.getenv('RESULT_BACKEND', 'redis://localhost:6379/0'),
    broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
)
# TODO(Jacob) using app.config_from_object('celeryconfig')
celery_app.conf.task_queues = (
    Queue('default', routing_key='default'),
    Queue('into_did', routing_key='app.verifications.did'),
    Queue('into_faucet', routing_key='app.faucet.bind'),
)
celery_app.conf.imports = [
    'app.src.service.celery_service',
    'app.src.service.contract',
    'app.src.service.into_faucet_contract'
]
celery_app.conf.timezone = os.environ.get('TIMEZONE', 'Asia/Shanghai')
celery_app.conf.enable_utc = False
celery_app.conf.task_publish_retry = True

celery_app.conf.task_routes = {
    'app.src.service.celery_service.celery_test': {
        'queue': 'default',
        'routing_key': 'default',
    },
    'app.src.service.contract.set_face_auth_message': {
        'queue': 'into_did',
        'routing_key': 'app.verifications.did',
    },
    'app.src.service.into_faucet_contract.into_faucet_bind': {
        'queue': 'into_faucet',
        'routing_key': 'app.faucet.bind',
    },
}

celery_app.conf.task_default_queue = 'default'
celery_app.conf.task_default_exchange = 'default'
celery_app.conf.task_default_routing_key = 'default'
