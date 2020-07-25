FROM python:3.7-alpine
MAINTAINER Sourabh Sinha - MbeforL #Best Practice

ENV PYTHONUNBUFFERED 1
#Recommended for Python

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgres-client
#Don't include extra dependencies on docker container

RUN apk add --update --no-cache --virtual .tmp-build-deps \
 gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps
# Delete temporary dependensies

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
#For Security pupose otherwise root account used,Best Practice




