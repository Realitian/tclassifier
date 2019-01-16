from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

def convert(glove, word2vec):
    glove2word2vec(glove, word2vec)
    model = KeyedVectors.load_word2vec_format(word2vec)
    print ("had success")

if __name__ == "__main__":
    convert('../data/glove.twitter.27B/glove.twitter.27B.200d.txt', '../data/twitter-200d-27B.vec')