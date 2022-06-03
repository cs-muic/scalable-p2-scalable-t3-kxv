FROM ubuntu:18.04

WORKDIR /app

COPY ./script/make_thumbnail.sh /usr/local/bin

RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get update -y && apt-get install -y imagemagick libmagickcore-dev libmagickwand-dev libmagic-dev && rm -rf /var/lib/apt/lists/*
RUN chmod +x /usr/local/bin/make_thumbnail.sh
