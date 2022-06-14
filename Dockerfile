FROM ubuntu:20.04 AS build-stage

WORKDIR /src

COPY ./script/* /usr/local/bin/

RUN chmod +x /usr/local/bin/*.sh

FROM python:3.9

WORKDIR /app

sudo sed --in-place --regexp-extended 's http://(us\.archive\.ubuntu\.com|security\.ubuntu\.com) https://mirrors.wikimedia.org g' /etc/apt/sources.list

RUN apt-get update \
    && apt-get --no-install-recommends install -y ffmpeg imagemagick\
    && rm -rf /var/lib/apt/lists/*

COPY work_queue/ ./

RUN pip install -r requirements.txt

COPY --from=build-stage /usr/local/bin/*.sh ./script/

RUN chmod +x work_queue.py
CMD ["python", "work_queue.py"]