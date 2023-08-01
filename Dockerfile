FROM python:3.11-alpine

WORKDIR /bot


ENV BOT_TOKEN=6668496941:AAFXhj0Cm6dY7Hla2GLYAILgviB9CR7cpcE
ENV DATABASE_URL=postgresql+asyncpg://grantbot:grantbot@192.168.3.2:5432/grantbot


COPY requirements.txt .
COPY src src/
COPY run.py .


RUN python3 -m pip install --upgrade pip
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps



CMD python3 /bot/run.py
