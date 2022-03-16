FROM python:3.10-alpine3.15
WORKDIR /code
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /code/
RUN apk add python3-dev libpq-dev gcc musl-dev &&\
    pip install -r requirements.txt
COPY . /code/