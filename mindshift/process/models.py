# -*- coding: utf-8 -*-
import numpy as np
import scipy
from gensim import models, similarities, matutils


class Modelling:

    def __init__(self):
        self.similar_index = 0
        self.corpus = "None"
        self.lda = None
        
    def lda_model(self, corpus, dictionary):
        self.lda = models.LdaMulticore(corpus, id2word=dictionary, workers=8, num_topics=100)
        print(self.lda.show_topics())
        # self.similar_index = similarities.MatrixSimilarity(self.lda[corpus])
        self.corpus = self.lda[corpus]
        
    def get_vectors(self):
        return self._get_vector(self.corpus)
         
    def _get_vector(self, corpus):
        # Change doc back to array
        def get_max_id():
            maxid = -1
            for doc in corpus:
                maxid = max(maxid, max([-1] + [fieldid for fieldid, _ in doc]))  # [-1] to avoid exception
            return maxid

        num_features = 1 + get_max_id()
        index = np.empty(shape=(len(corpus), num_features), dtype=np.float32)
        for docno, vector in enumerate(corpus):
            if docno % 1000 == 0:
                print("PROGRESS: at document #%i/%i" % (docno, len(corpus)))

            if isinstance(vector, np.ndarray):
                pass
            elif scipy.sparse.issparse(vector):
                vector = vector.toarray().flatten()
            else:
                vector = matutils.unitvec(matutils.sparse2full(vector, num_features))
            index[docno] = vector        
        return index
