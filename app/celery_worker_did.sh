#!/usr/bin/env sh

poetry install --no-root --only main
poetry shell
poetry run celery -A app.core.celery_app:celery_app worker -Q into_did --concurrency=1 --max-tasks-per-child=1 --loglevel info
