FROM python:3.8.12-alpine3.14

COPY . /app
WORKDIR /app

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps


ENTRYPOINT ["python3"]
CMD ["server.py"]
