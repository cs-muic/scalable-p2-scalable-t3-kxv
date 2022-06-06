#!/bin/bash

mkdir frames                                                                              # creating a dir named frames                                                       
ffmpeg -i $1 -t 00:00:10 -r 10/1 -vf "scale=480:360" frames/frame%03d.jpg &> /dev/null    # extracting 10s video into frames stored in the brandnew dir named frames