FROM python:3.9-alpine

ARG ARG_VERSION=local

ENV VERSION=${ARG_VERSION}

WORKDIR /home/sensorial

COPY . .

CMD gunicorn \
    -b 0.0.0.0:80 \
    --reload \
    app:app

RUN pip install -r requirements.txt --upgrade pip