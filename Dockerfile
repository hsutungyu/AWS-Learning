# syntax=docker/dockerfile:1

FROM python:3.9.7-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind=0.0.0.0:8000", "wsgi:application"]