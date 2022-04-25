import open3d as o3d
import numpy as np 
from sklearn.neighbors import KDTree
from scipy.spatial import cKDTree
import teaserpp_python

def pcd2xyz(pcd):
    return np.asarray(pcd.points).T


## sklearn NN

# def find_knn_cpu(feat0, feat1, knn=1, distance_metric='euclidean', return_distance=False):
#   feat1tree = KDTree(feat1, metric=distance_metric)  
#   dists, nn_inds = feat1tree.query(feat0, k=knn)
#   if return_distance:
#     return nn_inds.flatten(), dists
#   else:
#     return nn_inds.flatten()

# def find_correspondences(feats0, feats1, distance_metric='euclidean', mutual_filter=True):
#   nns01 = find_knn_cpu(feats0, feats1, knn=1, distance_metric=distance_metric, return_distance=False)
#   corres01_idx0 = np.arange(len(nns01))
#   corres01_idx1 = nns01
#   if not mutual_filter:
#     return corres01_idx0, corres01_idx1
#   nns10 = find_knn_cpu(feats1, feats0, knn=1, return_distance=False)
#   corres10_idx1 = np.arange(len(nns10))
#   corres10_idx0 = nns10
#   mutual_filter = (corres10_idx0[corres01_idx1] == corres01_idx0)
#   corres_idx0 = corres01_idx0[mutual_filter]
#   corres_idx1 = corres01_idx1[mutual_filter]
#   return corres_idx0, corres_idx1

## Scipy NN

def find_knn_cpu(feat0, feat1, knn=1, return_distance=False):
  feat1tree = cKDTree(feat1)
  dists, nn_inds = feat1tree.query(feat0, k=knn, n_jobs=-1)
  if return_distance:
    return nn_inds, dists
  else:
    return nn_inds

def find_correspondences(feats0, feats1, mutual_filter=True):
  nns01 = find_knn_cpu(feats0, feats1, knn=1, return_distance=False)
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

def get_teaser_solver(noise_bound):
    solver_params = teaserpp_python.RobustRegistrationSolver.Params()
    solver_params.cbar2 = 1.0
    solver_params.noise_bound = noise_bound
    solver_params.estimate_scaling = False
    solver_params.inlier_selection_mode = \
        teaserpp_python.RobustRegistrationSolver.INLIER_SELECTION_MODE.PMC_EXACT
    solver_params.rotation_tim_graph = \
        teaserpp_python.RobustRegistrationSolver.INLIER_GRAPH_FORMULATION.CHAIN
    solver_params.rotation_estimation_algorithm = \
        teaserpp_python.RobustRegistrationSolver.ROTATION_ESTIMATION_ALGORITHM.GNC_TLS
    solver_params.rotation_gnc_factor = 1.4
    solver_params.rotation_max_iterations = 10000
    solver_params.rotation_cost_threshold = 1e-16
    solver = teaserpp_python.RobustRegistrationSolver(solver_params)
    return solver