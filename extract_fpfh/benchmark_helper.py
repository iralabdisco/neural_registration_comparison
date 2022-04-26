import open3d as o3d
import numpy as np
import os

def load_problem(row, args):
    problem_id = row['id']

    source_pcd_filename = row['source']
    source_pcd_file = os.path.join(args.input_pcd_dir, source_pcd_filename)
    source_pcd_orig = o3d.io.read_point_cloud(source_pcd_file, remove_nan_points=True, 
                                        remove_infinite_points=True)

    target_pcd_filename = row['target']
    target_pcd_file = os.path.join(args.input_pcd_dir, target_pcd_filename)
    target_pcd_orig = o3d.io.read_point_cloud(target_pcd_file, remove_nan_points=True, 
                                        remove_infinite_points=True)    
    
    source_transform = np.eye(4)
    source_transform[0][0] = row['t1']
    source_transform[0][1] = row['t2']
    source_transform[0][2] = row['t3']
    source_transform[0][3] = row['t4']
    source_transform[1][0] = row['t5']
    source_transform[1][1] = row['t6']
    source_transform[1][2] = row['t7']
    source_transform[1][3] = row['t8']
    source_transform[2][0] = row['t9']
    source_transform[2][1] = row['t10']
    source_transform[2][2] = row['t11']
    source_transform[2][3] = row['t12']

    return problem_id, source_pcd_orig, target_pcd_orig, source_transform, target_pcd_filename