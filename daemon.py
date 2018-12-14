from engine.db import DailyDB
from engine.data_loader import load_data, clean_text
from engine.model import tf_logistic_regression
import time
import datetime

class Daemon:
    def __init__(self):
        sample_path = './engine/data/sample.csv'
        (self.X, self.X_train, self.X_test, self.Y_train, self.Y_test, self.tags) = load_data(sample_path)

        self.model = tf_logistic_regression.Model(self.X, self.tags)
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

if __name__ == '__main__':
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
