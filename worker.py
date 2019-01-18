import os

import redis
from rq import Worker, Queue, Connection
from engine.main import Service

service = Service('./engine')

listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

def query_api(text):
    # service.query(text)
    return 'ok'

def cluster_api(company_id, time_from, time_to, category, num_clusters):
    return 'ok'
    # service.cluster_api(company_id, time_from, time_to, category, num_clusters)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()