FROM python:3.5.1-alpine
ADD . /code
WORKDIR /code
RUN apk update
RUN apk add bash
RUN apk add gcc musl-dev 
RUN apk add postgresql-dev
RUN pip install -r requirements.txt
