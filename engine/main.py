from data_loader import load_data, clean_text
from model import tf_logistic_regression
import json
from cluster import cluster

class Service():
    def __init__(self, path):
        sample_path = path + '/data/sample.csv'
        (self.X, self.X_train, self.X_test, self.Y_train, self.Y_test, self.tags) = load_data(sample_path)

        self.model = tf_logistic_regression.Model(self.X, self.tags, path)
        self.model.train(self.X_train, self.Y_train)

    def query(self, texts):
        text_list = texts.split('\n')11
        input = []
        for text in text_list:
            input.append(clean_text(text))
        result = self.model.predict_all(input)

        index = 0
        formatted_result = []
        for row in result:
            formatted_result.append([index+1, text_list[index]] + row)
            index += 1

        return json.dumps({'result': formatted_result})

    def evaluate(self):
        self.model.evaluate(self.X_test, self.Y_test)

    def cluster_api(self, company_id, time_from, time_to, category, num_clusters):
        cluster(company_id, time_from, time_to, category, num_clusters)

if __name__ == "__main__":
    service = Service('.')
    service.evaluate()

    # print ("Earnings", service.query("Btw, Estimated #Earnings Per Share for $MSFT is $0.84 it's 0.77% of the current price"))
    #
    # print ("Ownership", service.query("Microsoft Co. $MSFT Shares Sold by American Research &amp"))
    #
    # print ("Ownership", service.query("Jaffetilchin Investment Partners LLC Decreases Stake in https://t.co/1UJLwx2Df0, inc. $CRM"))
    #
    # print ("Opinion", service.query("If humanity spent as much time studying physics as they did studying Tesla $TSLA stock, we would actually have free, unlimited, clean energy already."))
    #
    # print ("Ratings", service.query('Broadcom Inc $AVGO Given Average Rating of "Buy" by Analysts'))
    #
    # print ("Misc", service.query("$MU WSJ: U.S. to Restrict Chinese Chip Maker From Doing Business with American Firms"))
    #
    # print ("Spam", service.query("Swing Trading FREE lesson!!!! $FB $TWTR $CIEN"))
    #
    # print ("Negative", service.query("If you want to learn to trade biotech stocks check out this mentoring program. I love it. $fb $twtr $live"))