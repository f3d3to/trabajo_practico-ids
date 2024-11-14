
FROM python:3.10-slim

WORKDIR /app

ADD ../requirements.txt /app/

RUN pip install -r requirements.txt

ADD ../backend /app

EXPOSE 5000
