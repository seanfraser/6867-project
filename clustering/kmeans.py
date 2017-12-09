import numpy as np
import random

def k_medoids(data, k, eps=1e-8, mu=None):
    """ Run the k-medoids algorithm, pseudocode from 6.036 MIT Spring 2017
    data - an nxd ndarray (n data points * dimension of the data points)
    k - number of clusters to fit
    eps - stopping criterion tolerance
    mu - an optional KxD ndarray containing initial centroids

    returns: a tuple containing
        mu - a KxD ndarray containing the learned means
        cluster_assignments - an N-vector of each point's cluster index
    """
    n, d = data.shape

    if k > n:
        raise Exception('too many medoids')

    if mu is None:
        # randomly choose k points as initial centroids
        mu = data[random.sample(xrange(n), k)]

    previous_cost = 100.0 ; current_cost = 0.0
    
    while abs(previous_cost-current_cost) > eps:
        previous_cost = current_cost

        # array containing each point's cluster index (size n vector)
        cluster_assignments = np.argmin(np.sqrt(((data - mu[:, np.newaxis])**2).sum(axis=2)),axis = 0)

        #cluster means (k x d array) 
        mu = np.array([data[cluster_assignments==j].mean(axis=0) for j in range(k)])

        #cluster medoids/ exemplars (k x d array)
        # mu = np.zeros((k,d))
        # for j in xrange(k):
        #     cluster = data[cluster_assignments == j]
        #     z = cluster.shape[0]
        #     costs = np.zeros(z)
        #     for i in xrange(z):
        #         costs[i] = np.sum(np.linalg.norm(c - cluster[i]) for c in cluster)
        #     exemplar_idx = np.argmin(costs)
        #     mu[j] = cluster[exemplar_idx]

        #calculate cost with Euclidean distance (scalar)
        current_cost = np.sum([np.linalg.norm(data[i]-mu[cluster_assignments][i]) for i in range(n)])
    
    #print (current_cost)
    return (mu, cluster_assignments)