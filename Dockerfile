FROM python:3.7-alpine
MAINTAINER Goutom Roy

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY ./ /app

RUN pip install -r /app/requirements.txt

RUN adduser -D root
USER root
