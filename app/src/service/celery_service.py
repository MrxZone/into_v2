#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from celery.result import AsyncResult

from app.core.celery_app import celery_app


@celery_app.task(bind=True)
def celery_test(self, x, y):
    try:
        time.sleep(60)
    except Exception as e:
        raise self.retry(exc=e, countdown=3, max_retries=5)
    return x + y


def test():
    """
    celery test
    """
    # result = celery_test.delay(1, 2)
    result = celery_test.apply_async(
        args=[1, 2],
        queue='default',
        routing_key='default'
    )

    return result.id


def celery_result(task_id):
    """
    celery result
    """
    result = AsyncResult(task_id, app=celery_app)
    summary = {
        "id": result.id,
        "states": result.state,
        "result": result.result if result.result else {},
        "traceback": result.traceback if result.traceback else "",
    }
    return summary
