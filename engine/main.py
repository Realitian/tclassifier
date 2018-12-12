from data_loader import load_data, clean_text
import ml_relu_softmax
import json

class Service():
    def __init__(self, path):
        sample_path = path + '/data/sample.csv'
        (self.X, self.X_train, self.X_test, self.Y_train, self.Y_test, self.tags) = load_data(sample_path)

        self.model = ml_relu_softmax.Model(self.X, self.tags)
        self.model.train(self.X_train, self.Y_train)

    def query(self, text):
        category = self.model.predict(clean_text(text))
        return json.dumps({'ok': True, 'category': category})

    def evaluate(self):
        self.model.evaluate(self.X_test, self.Y_test)

if __name__ == "__main__":
    service = Service('.')
    service.evaluate()

    print ("Earnings", service.query("Btw, Estimated #Earnings Per Share for $MSFT is $0.84 it's 0.77% of the current price"))

    print ("Ownership", service.query("Microsoft Co. $MSFT Shares Sold by American Research &amp"))

    print ("Ownership", service.query("Jaffetilchin Investment Partners LLC Decreases Stake in https://t.co/1UJLwx2Df0, inc. $CRM"))

    print ("Opinion", service.query("If humanity spent as much time studying physics as they did studying Tesla $TSLA stock, we would actually have free, unlimited, clean energy already."))

    print ("Ratings", service.query('Broadcom Inc $AVGO Given Average Rating of "Buy" by Analysts'))

    print ("Misc", service.query("$MU WSJ: U.S. to Restrict Chinese Chip Maker From Doing Business with American Firms"))

    print ("Spam", service.query("Swing Trading FREE lesson!!!! $FB $TWTR $CIEN"))

    print ("Negative", service.query("If you want to learn to trade biotech stocks check out this mentoring program. I love it. $fb $twtr $live"))