FROM python:3.9-alpine

MAINTAINER PHO

ENV PYTHONEUNBUFFERED 1

#Copy all needable files
COPY ./Ph_o /Ph_o
COPY ./requirements.txt /requirements.txt


# Install dependencies

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps


WORKDIR Ph_o


RUN adduser -D user
USER user