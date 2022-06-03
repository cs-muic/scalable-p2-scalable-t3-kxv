FROM ubuntu:18.04

WORKDIR /app

COPY ./script/make_thumbnail.sh /usr/local/bin

RUN apt-get update && apt-get install -y ffmpeg
RUN chmod +x /usr/local/bin/make_thumbnail.sh
