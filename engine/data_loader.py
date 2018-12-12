import pandas as pd
from sklearn.model_selection import train_test_split
import re
# from nltk.corpus import stopwords

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
# STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = REPLACE_BY_SPACE_RE.sub(' ', text)  # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text)  # delete symbols which are in BAD_SYMBOLS_RE from text
    # text = ' '.join(word for word in text.split() if word not in STOPWORDS)  # delete stopwors from text
    return text

def load_data(path):
    df = pd.read_csv(path)

    X = []
    y = []

    tags = []

    for col in df:
        tags.append(col)

        for row in df[col]:
            if isinstance(row, str):
                text = row#clean_text(row)

                X.append(text)
                y.append(col)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state = 42)

    return (X, X_train, X_test, y_train, y_test, tags)