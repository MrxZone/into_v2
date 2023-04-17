#!/usr/bin/env sh

poetry install --no-root --only main
poetry shell
poetry run celery -A app.core.celery_app:celery_app worker -Q default --concurrency=1 --max-tasks-per-child=1 --loglevel info
#poetry run python -m http.server 8000
