#СБОРКА

FROM python:3.10

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY req.txt /app/

RUN pip install -r /app/req.txt

ADD . /app
