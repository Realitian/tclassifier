import numpy as np
from sklearn.preprocessing import LabelEncoder

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Activation, Dropout
from tensorflow.python.keras.preprocessing import text, sequence
from tensorflow.python.keras import utils
from tensorflow.python.keras.callbacks import TensorBoard
import time

class Model():
    def __init__(self, X, Y):
        self.max_words = 1226
        self.tokenize = text.Tokenizer(num_words=self.max_words, char_level=False)
        self.tokenize.fit_on_texts(X)
        self.encoder = LabelEncoder()
        self.encoder.fit(Y)
        self.batch_size = 32
        self.epochs = 30
        y = self.encoder.transform(Y)
        self.num_classes = np.max(y) + 1

        # self.tensorboard = TensorBoard(log_dir="logs/{}".format(time.time()))

        self.model = Sequential()
        self.model.add(Dense(512, input_shape=(self.max_words,)))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(self.num_classes))
        self.model.add(Activation('softmax'))

        self.model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

    def train(self, X_train, Y_train):
        x_train = self.tokenize.texts_to_matrix(X_train)

        y_train = self.encoder.transform(Y_train)

        y_train = utils.to_categorical(y_train, self.num_classes)

        history = self.model.fit(x_train, y_train,
                            batch_size=self.batch_size,
                            epochs=self.epochs,
                            verbose=1,
                            validation_split=0.1)

    def predict(self, X):
        x = self.tokenize.texts_to_matrix([X])
        y = self.model.predict(x)
        index = y.argmax()
        return self.encoder.inverse_transform([index])[0]

    def evaluate(self, X_test, Y_test):
        x_test = self.tokenize.texts_to_matrix(X_test)

        y_test = self.encoder.transform(Y_test)
        y_test = utils.to_categorical(y_test, self.num_classes)

        score = self.model.evaluate(x_test, y_test,
                               batch_size=self.batch_size, verbose=1)

        print('Test accuracy:', score[1])