# script to cluster data
from sklearn.cluster import KMeans


class Cluster:

    def __init__(self):
        self.NCLUSTERS = 5
        self.NITER = 5

    def do_kmeans(self, dataset):
        km_model = KMeans(n_clusters=self.NCLUSTERS, n_init=self.NITER, verbose=1)
        km_model.fit_transform(dataset)
        return km_model.labels_
