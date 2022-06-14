#!/bin/bash

folder="${2%}"
mkdir ${folder}                                                                # creating a dir named frames
ffmpeg -i $1 -t 00:00:10 -r 10/1 -vf "scale=480:360" ${folder}/frame%03d.jpg   # extracting 10s video into frames stored in the brandnew dir named frames