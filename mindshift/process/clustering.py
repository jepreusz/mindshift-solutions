# script to cluster data
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import ward
from scipy.cluster.hierarchy import fcluster

# add new packages for normalization
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

# imports for LDA. refactored from transformer.py
from mindshift.process.models import Modelling
from gensim import corpora
from nltk.corpus import stopwords
from mindshift.preprocess import data_filter


class Cluster:

    def __init__(self):
        self.NCLUSTERS = 100
        self.NITER = 5
        # Trial variable for number of cluster
        self.max_d = 50
        self.model = None
        self.svd = None
        self.tokenizer = data_filter.DataFilter()

    def do_kmeans(self, dataset):
        # normalization
        self.svd = TruncatedSVD(self.NCLUSTERS)
        normalizer = Normalizer(copy=False)
        lsa = make_pipeline(self.svd, normalizer)
        dataset = lsa.fit_transform(dataset)
        # finish normalization,start k-means
        self.model = KMeans(n_clusters=self.NCLUSTERS, n_init=self.NITER)
        self.model.fit_transform(dataset)
        return self.model.labels_

    def print_top_terms(self, features):
        for ind, term in enumerate(self.get_top_cluster_terms(features)):
            print("Cluster #: {0}   Top terms: {1}".format(ind, term))

    def get_top_cluster_terms(self, features, num_terms=15):
        original_space_centroids = self.svd.inverse_transform(self.model.cluster_centers_)
        order_centroids = original_space_centroids.argsort()[:, ::-1]
        top_terms = []
        for cluster_num in range(self.NCLUSTERS):
            top_terms.append(", ".join([features[i] for i in order_centroids[cluster_num, :num_terms]]))
        return top_terms

    def do_ward(self, dataset):
        # Pass cosine distance matrix
        linkage_matrix = ward(dataset)
        clusters = fcluster(linkage_matrix, self.max_d, criterion='distance')
        return clusters

    def do_lda(self, dataset):
        tokenized_text = [self.tokenizer.tokenize_(word) for word in dataset]
        final_text = [[word for text in tokenized_text for word in text if word.lower() not in
                       stopwords.words('english')]]
        dictionary = corpora.Dictionary(final_text)
        corpus = [dictionary.doc2bow(doc) for doc in final_text]
        self.model = Modelling(corpus, dictionary)
        print("Topics created:")
        self.model.print_topics()
        return self.model
