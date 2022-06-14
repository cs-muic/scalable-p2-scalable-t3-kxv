#!/usr/bin/env python3
from rq import Connection, Worker, Queue

from resource import RedisResource

listen = ['extracting', 'composing', 'status storing']

if __name__ == '__main__':
    with Connection(RedisResource.conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()