# script to cluster data
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import ward
from scipy.cluster.hierarchy import fcluster

# add new packages for normalization
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer


class Cluster:

    def __init__(self):
        self.NCLUSTERS = 40
        self.NITER = 5
        # Trial variable for number of cluster
        self.max_d = 50
        self.model = None
        self.svd = None

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
        original_space_centroids = self.svd.inverse_transform(self.model.cluster_centers_)
        order_centroids = original_space_centroids.argsort()[:, ::-1]
        for i in range(self.NCLUSTERS):
            print("Cluster id: {0}".format(i))
            for ind in order_centroids[i, :15]:
                print(' %s' % features[ind], end='')
            print()

    def do_ward(self, dataset):
        # Pass cosine distance matrix
        linkage_matrix = ward(dataset)
        clusters = fcluster(linkage_matrix, self.max_d, criterion='distance')
        return clusters
