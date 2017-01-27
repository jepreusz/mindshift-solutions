# -*- encoding: utf-8 -*-
import numpy as np
import pandas as pd
import scipy
from gensim import models, similarities, matutils


class Modelling:

    def __init__(self, corpus, dictionary):
        self.similar_index = 0
        self.lda = models.LdaMulticore(corpus, id2word=dictionary, workers=8, num_topics=100)
        self.corpus = self.lda[corpus]
        
    def get_doc_lda(self):
        doc_percent=dict()
        doc_topics=dict()
        #Print the document topic and percentage:
        for doc_id, doc in enumerate(self.corpus):
            doc_topics[doc_id] = list()
            doc_percent[doc_id] = list()
            for (topic_n, prob) in doc:
                word_list=list()
                for (word, _ ) in self.lda.show_topic(topic_n):
                    word_list.append(word)
                doc_topics[doc_id].append(word_list)
                doc_percent[doc_id].append(format(round(prob*100,2), '.2f'))
        df = pd.DataFrame([doc_topics, doc_percent]).T
        df.columns = ['List of Words','Percentage']
        #print(df['List of Words'])
        #print(df['Percentage'])
        #df = df.reset_index(drop=True)
        return df
        
    def print_topics(self):
        print("# topics: {0}".format(self.lda.num_topics))
        for topic in self.lda.show_topics(num_topics=50):
            print(topic)
        
    def get_vectors(self):
        return self.print_doc_lda()
        #return self._get_vector(self.corpus)
         
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
            print(vector)
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
