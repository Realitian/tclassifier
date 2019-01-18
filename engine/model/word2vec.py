import nltk
import numpy as np
import logging
import gensim
from sklearn.model_selection import train_test_split
from gensim.models import Word2Vec
import pandas as pd

class Word2Vec():
    def __init__(self, path):
        # model_file = path + "/data/GoogleNews-vectors-negative300.bin"
        # model_file = path + "/data/wiki-news-300d-1M.vec"
        # model_file = path + "/data/glove.twitter.27B/glove.twitter.27B.200d.txt"
        # model_file = path + "/data/crawl-300d-2M.vec"
        model_file = path + "/data/twitter-200d-27B.vec"
        binary = False

        self.wv = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=binary, limit=500000)
        self.wv.init_sims(replace=True)

        # model_file = path + "/data/twitter-200d-27B.vec"
        # binary = False
        # self.wv1 = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=binary, limit=500000)
        # self.wv1.init_sims(replace=True)

    def w2v_tokenize_text(self, text):
        tokens = nltk.word_tokenize(text)
        return tokens

        tokens = []
        for sent in nltk.sent_tokenize(text):
            for word in nltk.word_tokenize(sent):
                if len(word) < 2:
                    continue
                tokens.append(word)
        return tokens

    def word_averaging(self, wv, text):
        words = self.w2v_tokenize_text(text)
        mean = []

        for word in words:
            if word in wv.vocab:
                mean.append(wv.syn0norm[wv.vocab[word].index])

        if not mean:
            logging.warning("cannot compute similarity with no input %s", words)
            return np.zeros(wv.vector_size, )

        value = gensim.matutils.unitvec(np.array(mean).mean(axis=0)).astype(np.float32)
        return value

    def word_minimum(self, wv, text):
        words = self.w2v_tokenize_text(text)
        minimum = []

        for word in words:
            if word in wv.vocab:
                minimum.append(wv.syn0norm[wv.vocab[word].index])

        if not minimum:
            logging.warning("cannot compute similarity with no input %s", words)
            return np.zeros(wv.vector_size, )

        value = gensim.matutils.unitvec(np.array(minimum).min(axis=0)).astype(np.float32)
        return value

    def word_maximum(self, wv, text):
        words = self.w2v_tokenize_text(text)
        maximum = []

        for word in words:
            if word in wv.vocab:
                maximum.append(wv.syn0norm[wv.vocab[word].index])

        if not maximum:
            logging.warning("cannot compute similarity with no input %s", words)
            return np.zeros(wv.vector_size, )

        value = gensim.matutils.unitvec(np.array(maximum).max(axis=0)).astype(np.float32)
        return value

    def word_averaging_list(self, wv, text_list):
        return np.vstack([self.word_averaging(wv, text) for text in text_list])

    def word_minimum_list(self, wv, text_list):
        return np.vstack([self.word_minimum(wv, text) for text in text_list])

    def word_maximum_list(self, wv, text_list):
        return np.vstack([self.word_maximum(wv, text) for text in text_list])

    def word2vec_data(self, texts):
        mean = self.word_averaging_list(self.wv, texts)
        min = self.word_minimum_list(self.wv, texts)
        max = self.word_maximum_list(self.wv, texts)

        vec = []
        for i in range(0, len(mean)):
            v1 = mean[i]
            v2 = min[i]
            v3 = max[i]
            v = []
            for e1 in v1:
                v.append(float(e1))
            for e2 in v2:
                v.append(float(e2))
            for e3 in v3:
                v.append(float(e3))

            vec.append(v)

        return vec