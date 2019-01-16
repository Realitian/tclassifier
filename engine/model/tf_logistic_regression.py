import tensorflow as tf
from tensorflow.python.keras.preprocessing import text, sequence
from tensorflow.python.keras import utils
from sklearn.preprocessing import LabelEncoder
import numpy as np
import word2vec

MODE = 0

class Model():
    def __init__(self, X, Y, path):
        self.max_words = 1226
        self.tokenize = text.Tokenizer(num_words=self.max_words, char_level=False)
        self.tokenize.fit_on_texts(X)

        if MODE == 1:
            self.w2v = word2vec.Word2Vec(path)
            self.max_words = 200
        elif MODE == 2:
            self.w2v = word2vec.Word2Vec(path)
            self.max_words = 300 + 1226

        self.encoder = LabelEncoder()
        self.encoder.fit(Y)

        self.label_indices = self.encoder.transform(Y)
        self.num_classes = np.max(self.label_indices) + 1

        self.sess = tf.Session()

    def texts_to_vec(self, texts):
        if MODE == 1:
            vec = self.w2v.word2vec_data(texts)
            return vec
        elif MODE == 2:
            w2v_vec = self.w2v.word2vec_data(texts)
            bow_vec = self.tokenize.texts_to_matrix(texts)

            vec = []
            for i in range(0, len(w2v_vec)):
                v1 = w2v_vec[i]
                v2 = bow_vec[i]
                v = []
                for e1 in v1:
                    v.append(float(e1))
                for e2 in v2:
                    v.append(float(e2))

                vec.append( v )

            return vec

        vec = self.tokenize.texts_to_matrix(texts)
        return vec

    def train(self, X_train, Y_train):
        x_train = self.texts_to_vec(X_train)
        y_train = self.encoder.transform(Y_train)
        y_train = utils.to_categorical(y_train, self.num_classes)

        # Parameters
        learning_rate = 0.1
        training_epochs = 2000

        # tf Graph Input
        self.x = tf.placeholder(tf.float32, [None, self.max_words])
        self.y = tf.placeholder(tf.float32, [None, self.num_classes])

        # Set model weights
        W = tf.Variable(tf.zeros([self.max_words, self.num_classes]))
        b = tf.Variable(tf.zeros([self.num_classes]))

        # Construct model
        self.pred = tf.nn.softmax(tf.matmul(self.x, W) + b)
        # pred = tf.nn.sigmoid(tf.matmul(x, W) + b)

        # Minimize error using cross entropy
        cost = tf.reduce_mean(-tf.reduce_sum(self.y * tf.log(self.pred), reduction_indices=1))
        # Gradient Descent
        optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

        init = tf.global_variables_initializer()
        self.sess.run(init)

        # Training cycle
        for epoch in range(training_epochs):
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = self.sess.run([optimizer, cost], feed_dict={self.x: x_train, self.y: y_train})

            print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(c))

        print("Optimization Finished!")

    def predict_all(self, X):
        x = self.texts_to_vec(X)
        y = self.sess.run([self.pred], feed_dict={self.x: x})

        result = []
        for item in y[0]:
            row = []
            row.append(self.encoder.inverse_transform([item.argmax()])[0] + " (" + "{0:.2f}".format(np.asscalar(item[item.argmax()])) + ")")

            for i in self.label_indices:
                row.append("{0:.2f}".format(np.asscalar(item[i])))

            result.append(row)
        return result

    def predict_one(self, X):
        x = self.texts_to_vec([X])
        y = self.sess.run([self.pred], feed_dict={self.x: x})

        score = np.asscalar(y[0].max())
        label = self.encoder.inverse_transform([y[0].argmax()])[0]

        return (score, label)

    def evaluate(self, X_test, Y_test):
        x_test = self.texts_to_vec(X_test)
        y_test = self.encoder.transform(Y_test)
        y_test = utils.to_categorical(y_test, self.num_classes)

        correct_prediction = tf.equal(tf.argmax(self.pred, 1), tf.argmax(self.y, 1))
        # Calculate accuracy
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        print("Accuracy:", accuracy.eval({self.x: x_test, self.y: y_test}, self.sess))



