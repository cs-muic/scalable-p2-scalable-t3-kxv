#!/bin/sh

output_name="${1%.*}"                                            # getting output name
convert -delay 0 -loop 0 $2/*.jpg $output_name.gif               # making a gif
rm -r $2                                                         # removing everything in frames dir and the dir itself