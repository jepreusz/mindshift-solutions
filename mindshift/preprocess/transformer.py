# script to vectorize text and implement other transformation functions
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from mindshift.preprocess import data_filter
from mindshift.process import clustering
from nltk.corpus import webtext,stopwords
from nltk.stem import SnowballStemmer
from nltk import sent_tokenize, word_tokenize
import string


class Transformer:

    def __init__(self):
        self.tokenizer = data_filter.DataFilter()
        self.stemmer = SnowballStemmer('english')
        self.custom_vocabulary = self._get_vocabulary()
        self.vectorizer = TfidfVectorizer(stop_words='english', min_df=0.1, max_df=0.7, analyzer='word',
                                          vocabulary=self.custom_vocabulary, tokenizer=self.tokenizer.tokenize_)
        self.vector_features = []
        self.modeller = clustering.Cluster()
        self.lda_model=None

    def vectorize_text(self, text):
        vectorized_text = self.vectorizer.fit_transform(text)
        self.vector_features = self.vectorizer.get_feature_names()
        return vectorized_text

    def _remove_punc(self,text):
        tokens = [word.lower() for sentence in sent_tokenize(text) for word in word_tokenize(sentence)]
        return "".join([" " + i if not i in string.punctuation else i for i in tokens])
        
    def lda_vectorize_text(self, text):
        self.lda_model = self.create_lda_model(text)
        return self.lda_model.get_vectors()

    def create_lda_model(self, text):
        return self.modeller.do_lda(text)

    def get_features(self):
        return self.vector_features
        
    def get_cosine(self,dtm):
        dist = 1 - cosine_similarity(dtm)
        return np.round(dist, 2)

    def _get_vocabulary(self):
        vocab = {}
        index = 0
        for word in webtext.words():
            if self.stemmer.stem(word) not in vocab:
                vocab[self.stemmer.stem(word)] = index
                index += 1
        return vocab
