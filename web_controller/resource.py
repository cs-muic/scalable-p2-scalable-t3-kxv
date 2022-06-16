import os
import redis

from rq import Queue

class RedisResource:
    REDIS_QUEUE_LOCATION = os.getenv('REDIS_QUEUE', 'localhost')

    host, *port_info = REDIS_QUEUE_LOCATION.split(':')
    port = tuple()
    if port_info:
        port, *_ = port_info
        port = (int(port),)

    conn = redis.Redis(host=host, *port)

    extracting_queue = Queue('extracting', connection=conn)
    composing_queue = Queue('composing', connection=conn)
    status_queue = Queue('status storing', connection=conn)

