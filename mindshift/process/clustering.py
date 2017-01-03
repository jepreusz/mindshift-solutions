# script to cluster data
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import ward
from scipy.cluster.hierarchy import fcluster


class Cluster:

    def __init__(self):
        self.NCLUSTERS = 5
        self.NITER = 5
        #Trial variable for number of cluster
        self.max_d = 50

    def do_kmeans(self, dataset):
        km_model = KMeans(n_clusters=self.NCLUSTERS, n_init=self.NITER, verbose=1)
        km_model.fit_transform(dataset)
        return km_model.labels_
   
    def do_ward(self,dataset):
        #Pass cosine distance matrix
        linkage_matrix = ward(dataset)
        clusters = fcluster(linkage_matrix, self.max_d, criterion='distance')
        return clusters
        
        
        
        
        
        
