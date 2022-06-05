FROM ubuntu:18.04

WORKDIR /app

COPY ./script/make_thumbnail.sh /usr/local/bin

RUN apt-get update \
    && apt-get --no-install-recommends install -y ffmpeg imagemagick libmagickcore-dev libmagickwand-dev libmagic-dev \
    && rm -rf /var/lib/apt/lists/*
RUN chmod +x /usr/local/bin/make_thumbnail.sh
