import open3d as o3d
import numpy as np

def run_FastGlobal_registration(config, source, target, corrs_S, corrs_T):

    fgr_options = o3d.pipelines.registration.FastGlobalRegistrationOption(
                decrease_mu = config["decrease_mu"],
                division_factor = config["division_factor"],
                iteration_number = config["iteration_number"], 
                maximum_correspondence_distance = config["maximum_correspondence_distance"],
                tuple_scale = config["tuple_scale"], 
                tuple_test = config["tuple_test"], 
                use_absolute_scale = config["use_absolute_scale"])

    # convert from numpy to PointCloud
    source = o3d.utility.Vector3dVector(source.T)
    source = o3d.geometry.PointCloud(source)
    target = o3d.utility.Vector3dVector(target.T)
    target = o3d.geometry.PointCloud(target)

    ## WORKAROUND PER open3d 0.15.2: https://github.com/isl-org/Open3D/issues/4790
    if (len(source.points) > len(target.points)):

        corres_list = np.array([corrs_S, corrs_T], dtype="int32").transpose()
        corres = o3d.utility.Vector2iVector(corres_list)
        result_fast = o3d.pipelines.registration.registration_fgr_based_on_correspondence(
            source, target, corres, fgr_options)
        registration_solution = result_fast.transformation
    else:
        # SWAP TARGET E SOURCE
        corres_list = np.array([corrs_T, corrs_S], dtype="int32").transpose()
        corres = o3d.utility.Vector2iVector(corres_list)
        result_fast = o3d.pipelines.registration.registration_fgr_based_on_correspondence(
            target, source, corres, fgr_options)
        registration_solution = result_fast.transformation

        #INVERTI LA TRASFORMAZIONE VISTO CHE HAI SWAPPATO TARGET E SOURCE
        registration_solution =  np.linalg.inv(registration_solution)
    
    return registration_solution