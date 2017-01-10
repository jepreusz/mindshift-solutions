# script to vectorize text and implement other transformation functions
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from mindshift.preprocess import data_filter
from nltk.corpus import webtext
from nltk.stem import SnowballStemmer


class Transformer:

    def __init__(self):
        self.tokenizer = data_filter.DataFilter()
        self.stemmer = SnowballStemmer('english')
        self.custom_vocabulary = self._get_vocabulary()
        self.vectorizer = TfidfVectorizer('english', min_df=5, analyzer='word', vocabulary=self.custom_vocabulary,
                                          tokenizer=self.tokenizer.tokenzie_and_stem)
        self.vector_features = []

    def vectorize_text(self, text):
        vectorized_text = self.vectorizer.fit_transform(text)
        self.vector_features = self.vectorizer.get_feature_names()
        return vectorized_text

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
