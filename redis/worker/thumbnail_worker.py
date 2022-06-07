#!/usr/bin/env python3
import os
import logging
import json
import uuid
import redis
import subprocess

LOG = logging
REDIS_QUEUE_LOCATION = os.getenv('REDIS_QUEUE', 'localhost')
QUEUE_NAME = ['queue:extracting', 'queue:composing']

INSTANCE_NAME = uuid.uuid4().hex

LOG.basicConfig(
    level=LOG.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def watch_queue(redis_conn, queue_name, callback_func, timeout=30):
    active = True

    while active:
        packed = redis_conn.blpop(queue_name, timeout=timeout)

        if not packed:
            continue

        task_name, packed_task = packed

        if packed_task == b'DIE':
            active = False
        else:
            task = None
            try:
                task = json.loads(packed_task)
            except Exception:
                LOG.exception('json.loads failed')
            if task:
                callback_func(task_name, task)

def extract_resize(log, filename):
    try:
        log.info('Extracting and resizing input')
        subprocess.run(['./script/extract_resize.sh', str(filename)])
        log.info('Done extracting and resizing input')
    except Exception:
        log.exception('Failed to extract and resize')
        
def gif_compose(log, filename):
    try:
        log.info('Composing GIF file')
        subprocess.run(['./script/gif_compose.sh', str(filename)])
        log.info('Done composing GIF file')
    except Exception:
        log.exception('Failed to compose GIF file')

def execute_work(log, task_name, task):
    filename = task.get('filename')
    if task_name.decode('UTF-8') == QUEUE_NAME[0]:
        extract_resize(log, filename)
    else:
        gif_compose(log, filename)

def main():
    LOG.info('Starting a worker...')
    LOG.info('Unique name: %s', INSTANCE_NAME)
    host, *port_info = REDIS_QUEUE_LOCATION.split(':')
    port = tuple()
    if port_info:
        port, *_ = port_info
        port = (int(port),)

    named_logging = LOG.getLogger(name=INSTANCE_NAME)
    named_logging.info('Trying to connect to %s [%s]', host, REDIS_QUEUE_LOCATION)
    redis_conn = redis.Redis(host=host, *port)
    named_logging.info('Connecting to %s [%s]', host, REDIS_QUEUE_LOCATION)
    watch_queue(
        redis_conn, 
        QUEUE_NAME, 
        lambda task_name, task_descr: execute_work(named_logging, task_name, task_descr))

if __name__ == '__main__':
    main()