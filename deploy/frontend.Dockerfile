FROM python:3.10-slim

WORKDIR /app

ADD ./requirements.txt /app/

RUN pip install -r requirements.txt

ADD ../frontend /app

EXPOSE 5001
