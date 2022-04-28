import numpy as np 
from sklearn.neighbors import KDTree

def pcd2xyz(pcd):
    return np.asarray(pcd.points).T

def find_knn_cpu(feat0, feat1, knn=1, distance_metric='euclidean', return_distance=False):

  feat1tree = KDTree(feat1, metric=distance_metric)  

  dists, nn_inds = feat1tree.query(feat0, k=knn)

  if return_distance:
    return nn_inds.flatten(), dists
  else:
    return nn_inds.flatten()

def find_correspondences(feats0, feats1, distance_metric='euclidean', mutual_filter=True):
  nns01 = find_knn_cpu(feats0, feats1, knn=1, distance_metric=distance_metric, return_distance=False)
  corres01_idx0 = np.arange(len(nns01))
  corres01_idx1 = nns01

  if not mutual_filter:
    return corres01_idx0, corres01_idx1

  nns10 = find_knn_cpu(feats1, feats0, knn=1, return_distance=False)
  corres10_idx1 = np.arange(len(nns10))
  corres10_idx0 = nns10

  mutual_filter = (corres10_idx0[corres01_idx1] == corres01_idx0)
  corres_idx0 = corres01_idx0[mutual_filter]
  corres_idx1 = corres01_idx1[mutual_filter]

  return corres_idx0, corres_idx1