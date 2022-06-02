FROM ubuntu:18.04
RUN mkdir /make_thumbnail
ADD ./script/make_thumbnail.sh /make_thumbnail
ADD ./input.mp4 /make_thumbnail
WORKDIR /make_thumbnail
RUN apt-get update && apt-get install -y ffmpeg
RUN chmod 775 make_thumbnail.sh
CMD make_thumbnail.sh input.mp4 output.gif