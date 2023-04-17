FROM python:3.9-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

ENV PYTHONUNBUFFERED 1
EXPOSE 5897
WORKDIR /into_v2/

COPY poetry.lock pyproject.toml /into_v2/

RUN apk add --no-cache \
    gcc \
    libffi-dev \
    libxslt-dev \
    libc-dev \
    jpeg-dev \
    postgresql-dev \
    && pip config --global set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install --upgrade pip \
    && pip install poetry==1.4.0 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-root --only main\
    && rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache
