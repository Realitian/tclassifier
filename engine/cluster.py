from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from engine.db import DailyDB
import sys

def cluster(company_id, time_from, time_to, category, num_clusters):
    db = DailyDB()
    tweets = db.select_tweets(company_id, time_from, time_to, category)
    text = []
    for tweet in tweets:
        text.append(tweet[1])

    vectorizer = TfidfVectorizer(max_df=0.5, max_features=10000,
                                 min_df=2, stop_words='english',
                                 use_idf=True)
    X = vectorizer.fit_transform(text)

    km = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=100, n_init=1, verbose=False, random_state=3425)

    km.fit(X)

    clusterids = []
    for i in range(0, len(tweets)):
        clusterids.append((tweets[i][0], int(km.labels_[i])))
        # db.set_tweet_clusterid(tweets[i][0], int(km.labels_[i]))

    print(km.labels_)
    db.set_tweet_clusterids(clusterids)
    print('had set database')

    db.closeDB()

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) > 5:
        company_id = int(argv[1])
        time_from = argv[2]
        time_to = argv[3]
        category = argv[4]
        num_cluster = int(argv[5])

        # cluster(company_id, time_from, time_to, category, num_cluster)

    # cluster(20,"2019-01-17 14:15:55","2019-01-01 10:15:55","Opinion",8)
    cluster(48,"2019-01-01 14:15:55","2019-01-08 10:15:55","Opinion",8)