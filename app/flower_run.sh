#!/usr/bin/env sh

poetry install --no-root --only main
poetry shell
poetry run celery -A app.core.celery_app:celery_app flower --loglevel info --basic_auth=jacob:jacob123
