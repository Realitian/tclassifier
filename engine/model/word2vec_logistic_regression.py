from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression

def train_and_predict(X_train_word_average, X_test_word_average, y_train, y_test, tags):
    logreg = LogisticRegression(n_jobs=1, C=1e5)
    logreg = logreg.fit(X_train_word_average, y_train)
    y_pred = logreg.predict(X_test_word_average)
    print('accuracy %s' % accuracy_score(y_pred, y_test))
    print(classification_report(y_test, y_pred,target_names=tags))