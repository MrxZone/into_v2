#!/usr/bin/env sh

# 镜像已经安装了一部分 为了方便以后快速部署这里使用image构建之后再次安装

poetry install --no-root --only main
poetry shell
poetry run alembic revision --autogenerate
poetry run alembic upgrade head
poetry run uvicorn app.main:app --host 0.0.0.0 --port 5897