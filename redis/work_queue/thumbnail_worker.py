#!/usr/bin/env python3
import subprocess

from resource import RedisResource

def extract_resize(filename):
    try:
        subprocess.run(['./script/extract_resize.sh', str(filename)], shell=True)
        RedisResource.composing_queue.enqueue(gif_compose, args=filename)
    except Exception:
        print('Failed to extract and resize')
        
def gif_compose(filename):
    try:
        subprocess.run(['./script/gif_compose.sh', str(filename)], shell=True)
    except Exception:
        print('Failed to compose GIF file')
