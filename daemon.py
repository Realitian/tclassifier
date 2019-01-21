from engine.db import DailyDB
from engine.data_loader import load_data, clean_text
from engine.model import tf_logistic_regression
import time
import datetime
from multiprocessing.connection import Listener

try:
    import queue
except ImportError:
    import Queue as queue

from engine.main import Service
import threading

q = queue.Queue(maxsize=0)
address = ('localhost', 16000)     # family is deduced to be 'AF_INET'

class Daemon:
    def __init__(self):
        sample_path = './engine/data/sample.csv'
        (self.X, self.X_train, self.X_test, self.Y_train, self.Y_test, self.tags) = load_data(sample_path)

        self.model = tf_logistic_regression.Model(self.X, self.tags, './engine')
        self.model.train(self.X_train, self.Y_train)

    def run(self):
        while True:
            try:
                self.start()
            except Exception as ex:
                print (ex)
                time.sleep(60)

    def start(self):
        db = DailyDB()

        tweet_count = db.get_todo_count()
        for offset in range(0, tweet_count, 1000):
            jobs = db.get_todo_list(offset)
            for (id, content) in jobs:
                (score, label) = self.model.predict_one(clean_text(content))
                db.set_catescore(id, score, label)
            print ('classified', datetime.datetime.now(), offset)

        db.closeDB()

        time.sleep(60)

def listener():
    while True:
        with Listener(address, authkey=b'secret password') as listener:
            with listener.accept() as conn:
                print('connection accepted from', listener.last_accepted)

                (company_id, time_from, time_to, category, num_clusters) = conn.recv()

                print("q.qsize : ", q.qsize())
                q.put((company_id, time_from, time_to, category, num_clusters))

def worker_func():
    print ("workor thread started")
    while True:

        print ("worker thread waiting for new message")

        try:
            (company_id, time_from, time_to, category, num_clusters) = q.get()
            print ('clustering: ', company_id, time_from, time_to, category, num_clusters)
            # service.cluster_api(company_id, time_from, time_to, category, num_clusters)
            print ('clustering: finished')
        except Exception as ex:
            print (ex)
        q.task_done()

if __name__ == '__main__':
    q.join()

    worker_thread = threading.Thread(target=worker_func)
    worker_thread.start()

    listener_thread = threading.Thread(target=listener)
    listener_thread.start()

    d = Daemon()
    d.run()

    # for text in [
    #     "Btw, Estimated #Earnings Per Share for $MSFT is $0.84 it's 0.77% of the current price",
    #     "Microsoft Co. $MSFT Shares Sold by American Research &amp",
    #     "Jaffetilchin Investment Partners LLC Decreases Stake in https://t.co/1UJLwx2Df0, inc. $CRM",
    #     "If humanity spent as much time studying physics as they did studying Tesla $TSLA stock, we would actually have free, unlimited, clean energy already.",
    #     'Broadcom Inc $AVGO Given Average Rating of "Buy" by Analysts',
    #     "$MU WSJ: U.S. to Restrict Chinese Chip Maker From Doing Business with American Firms",
    #     "Swing Trading FREE lesson!!!! $FB $TWTR $CIEN",
    #     "If you want to learn to trade biotech stocks check out this mentoring program. I love it. $fb $twtr $live"
    # ]:
    #     (score, label) = d.model.predict_one(clean_text(text))
    #     print (score, label)
