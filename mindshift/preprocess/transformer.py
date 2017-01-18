# script to vectorize text and implement other transformation functions
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from mindshift.preprocess import data_filter
from nltk.corpus import webtext,stopwords
from nltk.stem import SnowballStemmer
from mindshift.process.models import Modelling
from gensim import corpora, models, similarities
from nltk import sent_tokenize, word_tokenize
import string


class Transformer:

    def __init__(self):
        self.tokenizer = data_filter.DataFilter()
        self.stemmer = SnowballStemmer('english')
        self.custom_vocabulary = self._get_vocabulary()
        self.vectorizer = TfidfVectorizer(stop_words='english', min_df=5, analyzer='word', vocabulary=self.custom_vocabulary,
                                          ngram_range=(1, 3), tokenizer=self.tokenizer.tokenize_and_stem)
        self.vector_features = []
        self.lda_model=None

    def vectorize_text(self, text):
        vectorized_text = self.vectorizer.fit_transform(text)
        self.vector_features = self.vectorizer.get_feature_names()
        return vectorized_text

    def _remove_punc(self,text):
        tokens = [word.lower() for sentence in sent_tokenize(text) for word in word_tokenize(sentence)]
        return "".join([" " + i if not i in string.punctuation else i for i in tokens])
        
    def lda_vectorize_text(self, text):
        self.create_lda_model(text)
        return self.lda_model.get_vectors()

    def create_lda_model(self, text):
        tokenized_text = [self.tokenizer.tokenize_(word) for word in text]
        final_text = [[word for text in tokenized_text for word in text if word.lower() not in stopwords.words('english')]]
        dictionary = corpora.Dictionary(final_text)
        corpus = [dictionary.doc2bow(doc) for doc in final_text]
        self.lda_model = Modelling(corpus, dictionary)
        print("Topics created:")
        self.lda_model.print_topics()

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
