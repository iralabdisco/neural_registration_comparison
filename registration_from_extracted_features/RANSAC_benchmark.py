import open3d as o3d
import numpy as np

def run_RANSAC_registration(config, source, target, corrs_S, corrs_T):

    corres_list = np.array([corrs_S, corrs_T], dtype="int32").transpose()
    corres = o3d.utility.Vector2iVector(corres_list)
    
    # convert from numpy to PointCloud
    source = o3d.utility.Vector3dVector(source)
    source = o3d.geometry.PointCloud(source)
    target = o3d.utility.Vector3dVector(target)
    target = o3d.geometry.PointCloud(target)

    max_correspondence_distance = config["max_correspondence_distance"]

    checkers = []
    for i in config["checkers"]:
        checkers.append(eval(i))
    
    result = o3d.pipelines.registration.registration_ransac_based_on_correspondence(
            source, target, corres, max_correspondence_distance,
            eval(config["estimation_method"]), config["ransac_n"], checkers, 
            o3d.pipelines.registration.RANSACConvergenceCriteria(config["max_iteration"], config["confidence"]))

    registration_solution = result.transformation

    return registration_solution
