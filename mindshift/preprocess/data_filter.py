# script to clean the input data by removing stopwords, special characters, etc.
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords, words
from nltk.tokenize import LineTokenizer, RegexpTokenizer
from nltk.stem import SnowballStemmer
from nltk import ngrams


class DataFilter:

    def __init__(self):
        self.bl_tokenizer = LineTokenizer()
        self.re_tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
        self.stemmer = SnowballStemmer('english')
        self.NGRAM_RANGE = 3

    def rm_blanklines(self, text):
        return " ".join([word for word in self.bl_tokenizer.tokenize(text)])

    def rm_stopwords(self, text):
        return " ".join([word for word in word_tokenize(text) if word.lower() not in stopwords.words()])

    def ngram_tokenize(self, text):
        return [word for sent in sent_tokenize(text) for word in ngrams(self.re_tokenizer.tokenize(sent), self.NGRAM_RANGE)]

    def tokenize_(self, text):
        return [word for sent in sent_tokenize(text) for word in self.re_tokenizer.tokenize(sent)]

    def tokenize_and_stem(self, text):
        return [self.stemmer.stem(word) for sent in sent_tokenize(text) for word in self.re_tokenizer.tokenize(sent)]

    def rm_nonwords(self, text):
        return " ".join([word for word in word_tokenize(text) if word.lower() in words.words()])
