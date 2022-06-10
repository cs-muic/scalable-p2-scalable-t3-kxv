FROM ubuntu:18.04 AS build-stage 

WORKDIR /src

COPY ./script/* /usr/local/bin/

RUN apt-get update \
    && apt-get --no-install-recommends install -y ffmpeg imagemagick \
    && rm -rf /var/lib/apt/lists/*
RUN chmod +x /usr/local/bin/*.sh

FROM python:3.9-alpine

WORKDIR /app

COPY ./redis/worker/ ./

RUN pip install -r requirements.txt

COPY --from=build-stage /usr/local/bin/*.sh ./script/

RUN chmod +x thumbnail_worker.py
CMD ["python", "thumbnail_worker.py"]