# script to clean the input data by removing stopwords, special characters, etc.
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import LineTokenizer, RegexpTokenizer
from nltk.stem import SnowballStemmer


class DataFilter:

    def __init__(self):
        self.bl_tokenizer = LineTokenizer()
        self.re_tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
        self.stemmer = SnowballStemmer('english')

    def rm_blanklines(self, text):
        return " ".join([word for word in self.bl_tokenizer.tokenize(text)])

    def rm_stopwords(self, text):
        return " ".join([word for word in word_tokenize(text) if word.lower() not in stopwords.words()])

    def tokenzie_and_stem(self, text):
        return [self.stemmer.stem(word) for sent in sent_tokenize(text) for word in self.re_tokenizer.tokenize(sent)]
