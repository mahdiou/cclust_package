# -*- coding: utf-8 -*-

"""
Evaluating the partition quality
"""
import numpy as np
from coclust.CoclustMod import CoclustMod

def best_modularity_partition(in_data, nbr_clusters_range, n_rand_init = 1):
    """Evaluation the best partition over a range of number of cluster
    using co-clustering by direct maximization of graph modularity.

    Parameters
    ----------
    in_data : numpy array or scipy sparse matrix, shape=(n_samples, n_features)
        Matrix to be analyzed
    nbr_clusters_range : number of clusters to be evaluated
    n_rand_init: Number of time the algorithm will be run with different initializations

    Values
    ----------
    tmp_best_model: model with highest final modularity
    tmp_max_modularities: final modularities for all evaluated partitions
    """

    tmp_best_model = None
    tmp_max_modularities = [np.nan] * len(nbr_clusters_range)
    eps_best_model = 1e-4
    
    # Set best final modularity to -inf
    modularity_begin = float("-inf")

    print("Computing coclust modularity for a range of cluster numbers =", end = ' ')
    for tmp_n_clusters in nbr_clusters_range:
        print(" %d ..." % (tmp_n_clusters), end = ' ')
        # Create and fit a model with tmp_n_clusters co-clusters
        tmp_model = CoclustMod(n_clusters = tmp_n_clusters, n_init = n_rand_init,
                               random_state = 0)
        tmp_model.fit(in_data)

        modularity_end = tmp_model.modularity
        # Check if the final modularity is better with tolerance
        if((modularity_end - modularity_begin) > eps_best_model):
            tmp_best_model = tmp_model
            modularity_begin = modularity_end

        tmp_max_modularities[(tmp_n_clusters)-min(nbr_clusters_range)] = tmp_model.modularity

    print(" All done !")
    return [tmp_best_model, tmp_max_modularities,]


