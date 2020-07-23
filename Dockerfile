FROM python:3.7-alpine
MAINTAINER Sourabh Sinha - MbeforL #Best Practice

ENV PYTHONUNBUFFERED 1
#Recommended for Python

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
#For Security pupose otherwise root account used,Best Practice




