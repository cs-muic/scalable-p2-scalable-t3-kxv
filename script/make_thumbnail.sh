#!/bin/bash

palette="/tmp/palette.png"
filters="scale=320:-1:flags=lanczos"

ffmpeg -v warning -i "$1" -vf "$filters,palettegen" -y $palette
ffmpeg -v warning -i "$1" -i $palette -lavfi "$filters [x]; [x][1:v] paletteuse" -t 00:00:10 -y $2