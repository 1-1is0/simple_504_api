# syntax = docker/dockerfile:1
FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
WORKDIR /app

RUN --network=host <<eot
    apt-get update
    apt-get install -y netcat-traditional libpq-dev curl clang libjpeg-dev \
    libturbojpeg0 libturbojpeg0-dev libwebp-dev python3-dev zlib1g zlib1g-dev
    pip install -U pip
eot

COPY ./requirements.txt requirements.txt
RUN --network=host pip install -r requirements.txt

COPY . .
COPY ./entrypoint.sh .
RUN <<eot
    chmod +x ./entrypoint.sh;
eot


ENTRYPOINT [ "./entrypoint.sh" ]
# CMD [ "python", "main.py" ]
