FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
WORKDIR /app

RUN apt-get update && apt-get install -y netcat-traditional libpq-dev curl clang libjpeg-dev \
    libturbojpeg0 libturbojpeg0-dev libwebp-dev python3-dev zlib1g zlib1g-dev

RUN pip install -U pip

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh;


ENTRYPOINT [ "./entrypoint.sh" ]
# CMD [ "python", "main.py" ]
