FROM ubuntu:20.04 AS build-stage

WORKDIR /src

COPY ./script/* /usr/local/bin/

RUN chmod +x /usr/local/bin/*.sh

FROM python:3.9-alpine

WORKDIR /app

RUN apk add --no-cache ffmpeg imagemagick

COPY work_queue/ ./

RUN pip install -r requirements.txt

COPY --from=build-stage /usr/local/bin/*.sh ./script/

RUN chmod +x work_queue.py
CMD ["python", "work_queue.py"]