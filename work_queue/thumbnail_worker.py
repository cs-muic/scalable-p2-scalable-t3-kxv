#!/usr/bin/env python3
import subprocess
import uuid
from resource import RedisResource
from minio_setup import upload_to_bucket, setup_bucket


def extract_resize(filename):
    bucket_name = uuid.uuid4().hex
    # downloading_from_bucket('videos', filename)  # pulling vid from minio
    try:
        subprocess.run(f"sh './script/extract_resize.sh' '{str(filename)}' '{bucket_name}'", shell=True)
        setup_bucket(bucket_name)  # create a bucket for storing the frames with the random name above
        local_path = f'./{bucket_name}'
        upload_to_bucket(local_path, bucket_name, local_path)
        subprocess.run(f"rm -r ./{bucket_name}", shell=True)
        RedisResource.composing_queue.enqueue(gif_compose, args=[filename, bucket_name])
    except Exception:
        print('Failed to extract and resize')


def gif_compose(filename, bucket_name):
    try:
        subprocess.run(f"sh './script/gif_compose.sh' '{str(filename)}' {bucket_name}", shell=True)
    except Exception:
        print('Failed to compose GIF file')
