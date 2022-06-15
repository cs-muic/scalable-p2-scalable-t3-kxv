#!/usr/bin/env python3
import subprocess
import uuid
from resource import RedisResource
from minio_setup import upload_to_bucket, setup_bucket, download_from_bucket, download_bucket, upload_gif, delete_bucket, list_all_files

def given_id(bucket_name):
    all_files = list_all_files(bucket_name)
    work_dict = []
    for file in all_files:
        unique_id = uuid.uuid4().hex
        filename = file.object_name
        work_dict.append({
            'file_name': filename,
            'id': unique_id
        })
        RedisResource.status_queue.enqueue(update_status, args=[unique_id, "waiting for a queue"])
    RedisResource.extracting_queue.enqueue(extract_resize_all, args=[work_dict])
    return work_dict


def extract_resize(unique_id, filename):
    try:
        download_from_bucket('videos', filename)  # pulling vid from minio
        RedisResource.status_queue.enqueue(update_status, args=[unique_id, "waiting for a queue"])
        subprocess.run(f"sh './script/extract_resize.sh' '{str(filename)}' '{unique_id}'", shell=True)
        setup_bucket(unique_id)  # create a bucket for storing the frames with the random name above
        upload_to_bucket(unique_id, unique_id)
        subprocess.run(f"rm -r ./{unique_id}", shell=True) 
        RedisResource.composing_queue.enqueue(gif_compose, args=[filename, unique_id])
        subprocess.run(f"rm -r ./{filename}", shell=True)
    except Exception:
        RedisResource.status_queue.enqueue(update_status, args=[unique_id, "failed to extract and resize"])


def extract_resize_all(work_dict):
    try:
        for work in work_dict:
            filename = work['file_name']
            unique_id = work['id']
            extract_resize(unique_id, filename)
    except Exception:
        print('Failed to extract and resize')


def gif_compose(filename, bucket_name):
    try:
        RedisResource.status_queue.enqueue(update_status, args=[bucket_name, "done extracting"])
        download_bucket(bucket_name)
        subprocess.run(f"sh './script/gif_compose.sh' '{str(filename)}' {bucket_name}", shell=True)
        setup_bucket('gifs')
        gif_name = filename.split('.')[0] + '.gif'
        upload_gif(gif_name, 'gifs')
        RedisResource.status_queue.enqueue(update_status, args=[bucket_name, "done composing GIF"])
        delete_bucket(bucket_name)
    except Exception:
        print('Failed to compose GIF file')


def list_all(bucket_name):
    try:
        all_files = list_all_files(bucket_name)
        files: list[str]  = []
        for file in all_files:
            name = str(file.object_name)
            files.append(name)
        return files
    except Exception:
        print('Failed to list all media files')
        return []


def update_status(ID, status):
    try:
        RedisResource.conn.set(ID, status)
    except Exception as e:
        RedisResource.conn.set(ID, "failed to compose gif file")
