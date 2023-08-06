FROM python:3.11-alpine

WORKDIR /bot

COPY requirements.txt .
COPY src src/
COPY locales locales/
COPY run.py .


RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt --no-cache-dir


RUN pybabel compile -d locales

CMD python3 /bot/run.py
