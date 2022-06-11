#!/usr/bin/env python3
from rq import Connection, Worker

from resource import RedisResource

if __name__ == '__main__':
    with Connection(RedisResource.conn):
        worker = Worker(['extracting'])
        worker.work()