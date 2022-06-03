#!/bin/bash

mkdir frames                                                                # creating a dir named frames
output_name="${2%.*}"                                                       # getting output name
ffmpeg -i $1 -t 00:00:10 -r 30/1 frames/frame%03d.jpg                       # extracting 10s video into frames stored in the brandnew dir named frames
convert -resize 720x540 -delay 0 -loop 0 frames/*.jpg $output_name.gif      # making a gif
rm -r frames                                                                # removing everything in frames dir and the dir itself