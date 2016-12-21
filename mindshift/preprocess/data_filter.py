# script to clean the input data by removing stopwords, special characters, etc.
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class DataFilter:

    def __init__(self):
        pass

    def rm_stopwords(self, text):
        return " ".join([word for word in word_tokenize(text) if word.lower() not in stopwords.words()])
