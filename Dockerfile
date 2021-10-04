FROM python:3.8.12-alpine3.14

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev postgresql-client

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY . .
