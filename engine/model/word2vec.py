import nltk
import numpy as np
import logging
import gensim
from sklearn.model_selection import train_test_split
from gensim.models import Word2Vec
import pandas as pd

def w2v_tokenize_text(text):
    tokens = nltk.word_tokenize(text)
    return tokens

    tokens = []
    for sent in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sent):
            if len(word) < 2:
                continue
            tokens.append(word)
    return tokens

def word_averaging(wv, words):
    all_words, mean = set(), []

    for word in words:
        if isinstance(word, np.ndarray):
            mean.append(word)
        elif word in wv.vocab:
            mean.append(wv.syn0norm[wv.vocab[word].index])
            all_words.add(wv.vocab[word].index)

    if not mean:
        logging.warning("cannot compute similarity with no input %s", words)
        return np.zeros(wv.vector_size, )

    mean = gensim.matutils.unitvec(np.array(mean).mean(axis=0)).astype(np.float32)
    return mean

def word_averaging_list(wv, text_list):
    return np.vstack([word_averaging(wv, text) for text in text_list])

def word2vec_data(X_train, X_test):
    test_tokenized = w2v_tokenize_text(X_test)
    train_tokenized = w2v_tokenize_text(X_train)

    wv = gensim.models.KeyedVectors.load_word2vec_format("data/GoogleNews-vectors-negative300.bin.gz", binary=True)
    wv.init_sims(replace=True)

    X_train_word_average = word_averaging_list(wv, train_tokenized)
    X_test_word_average = word_averaging_list(wv, test_tokenized)

    return (X_train_word_average, X_test_word_average)