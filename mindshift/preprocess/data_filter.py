# script to clean the input data by removing stopwords, special characters, etc.
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import LineTokenizer, RegexpTokenizer


class DataFilter:

    def __init__(self):
        self.bl_tokenizer = LineTokenizer()
        self.re_tokenizer = RegexpTokenizer(r'\w+')

    def rm_blanklines(self, text):
        return " ".join([word for word in self.bl_tokenizer.tokenize(text)])

    def rm_stopwords(self, text):
        return " ".join([word for word in word_tokenize(text) if word.lower() not in stopwords.words()])
