FROM python:3.10.1-alpine3.14

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app/komtek_test/

RUN apk upgrade
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    pip install --no-cache-dir -r requirements.txt 
COPY . /app/komtek_test/
