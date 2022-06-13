#!/bin/bash

output_name="${1%.*}"                                                # getting output name
convert -delay 0 -loop 0 {$2}/*.jpg $output_name.gif &> /dev/null    # making a gif
rm -r frames                                                         # removing everything in frames dir and the dir itself