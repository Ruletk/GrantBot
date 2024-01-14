# Install dependencies stage
FROM python:3.11.0-slim AS builder

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN python3 -m pip install poetry
RUN poetry config virtualenvs.in-project true  && \
    poetry install --no-dev


# Final stage
FROM python:3.11.0-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src
COPY locales/ /app/locales
COPY run.py /app/run.py
COPY .env /app/.env

ENV PATH="/app/.venv/bin:$PATH"
RUN mkdir /app/logs

CMD ["python", "run.py"]
