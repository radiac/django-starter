FROM python:3.12-slim

RUN mkdir /build
WORKDIR /build

# Build process dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Expose runserver/gunicorn
EXPOSE 8000/tcp

# Full python requirements to support development
COPY ./requirements.txt /build/requirements.txt
RUN pip install -r /build/requirements.txt

# Run Django
WORKDIR /project
