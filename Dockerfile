# Pull base image
FROM python:3.7-alpine

MAINTAINER Goutom Roy

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
RUN mkdir /code
WORKDIR /code

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# copy project
COPY . /code/

# install dependencies
RUN pip3 install -r requirements.txt



