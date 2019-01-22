from engine.cluster import cluster
import time
from clustering_db import ClusteringDB

def run():
    while True:
        try:
            start()
        except Exception as ex:
            print(ex)
            time.sleep(6)

def start():
    db = ClusteringDB()

    message = db.getMessage()

    if message:
        (id, company_id, time_from, time_to, category, num_clusters) = message
        print(message)
        try:
            cluster(company_id, time_from, time_to, category, num_clusters)
            db.setMessage(id, 1)
        except Exception as ex:
            db.setMessage(id, 2)
            print(ex)

    db.closeDB()

    time.sleep(6)

if __name__ == '__main__':
    run()