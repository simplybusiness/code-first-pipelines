#!/usr/bin/env dockerfile-shebang
FROM python:3.8-slim

WORKDIR /library

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.12

COPY poetry.lock pyproject.toml Makefile ./

COPY ./ ./

ENTRYPOINT ["make"]

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        make gcc libpng-dev libfreetype6-dev pkg-config graphviz libgraphviz-dev && \
    pip install --upgrade pip==20.2.4 && \
    pip install "poetry==$POETRY_VERSION" && \
    poetry install --no-root && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
