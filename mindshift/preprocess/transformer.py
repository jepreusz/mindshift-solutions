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
import configparser
from mindshift.util import vocab_builder
import pickle


class Transformer:

    def __init__(self):
        self.tokenizer = data_filter.DataFilter()
        self.stemmer = SnowballStemmer('english')
        self.vocabulary_builder = vocab_builder.VocabBuilder("C:\\Users\\ramji\\PycharmProjects\\mindshift-solutions\\mindshift\\dataFiles\\business_terms.txt")
        # self.custom_vocabulary = self._build_custom_vocabulary()
        self.vectorizer = TfidfVectorizer(stop_words='english', min_df=0.1, max_df=0.8, analyzer='word',
                                          vocabulary=self.custom_vocabulary)
        self.vector_features = []
        self.modeller = clustering.Cluster()
        self.lda_model=None
        self.config_handler = configparser.ConfigParser()

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

    def get_vocabulary(self):
        return self.vectorizer.vocabulary_

    def _build_custom_vocabulary(self):
        vocab = {}
        # load existing vocabulary
        with open("C:\\Users\\ramji\\PycharmProjects\\mindshift-solutions\\mindshift\\preprocess\\corpus_vocab", 'rb') as file:
            vocab = pickle.load(file)
        index = len(vocab.keys())
        for word in self.vocabulary_builder.build_vocab():
            if word not in vocab:
                vocab[word] = index
                index += 1
        return vocab
