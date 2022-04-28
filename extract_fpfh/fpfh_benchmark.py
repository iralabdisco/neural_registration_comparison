import argparse
import copy
import os

import numpy as np
import open3d as o3d
import pandas as pd
from tqdm import tqdm

def pcd2xyz(pcd):
    return np.asarray(pcd.points).T

def preprocess_point_cloud(pcd, voxel_size):
    o3d.utility.set_verbosity_level(o3d.utility.Error)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, np.array(pcd_fpfh.data).T

def main(args):
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    df = pd.read_csv(args.input_txt, sep=' ', comment='#')
    df = df.reset_index()

    problem_name = os.path.splitext(os.path.basename(args.input_txt))[0]

    print(problem_name)
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        problem_id = row['id']

        source_pcd_filename = row['source']
        source_pcd_file = os.path.join(args.input_pcd_dir, source_pcd_filename)
        source_pcd = o3d.io.read_point_cloud(source_pcd_file, remove_nan_points=True, 
                                            remove_infinite_points=True)

        target_pcd_filename = row['target']
        target_pcd_file = os.path.join(args.input_pcd_dir, target_pcd_filename)
        target_pcd = o3d.io.read_point_cloud(target_pcd_file, remove_nan_points=True, 
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

        moved_source_pcd = copy.deepcopy(source_pcd)
        moved_source_pcd.transform(source_transform)

        moved_source_down, source_fpfh = preprocess_point_cloud(moved_source_pcd, args.voxel_size)
        moved_source_xyz = pcd2xyz(moved_source_down)

        # Save out the output
        source_features_npz = os.path.join(args.output_dir, '{}'.format(problem_id))
        np.savez_compressed(source_features_npz, xyz_down=moved_source_xyz, features=source_fpfh)  

        ## Extract features from target
        target_features_npz = os.path.join(args.output_dir, os.path.splitext(target_pcd_filename)[0])
        if not(os.path.isfile(target_features_npz + '.npz')):     
            target_down, target_fpfh = preprocess_point_cloud(target_pcd, args.voxel_size)
            target_xyz = pcd2xyz(target_down)

            # Save out the output
            np.savez_compressed(target_features_npz, xyz_down=target_xyz, features=target_fpfh)  
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute FPFH')
    # Benchmark files and dirs
    parser.add_argument('--input_txt', type=str,
                    help='Path to the problem .txt')
    parser.add_argument('--input_pcd_dir', type=str,
                    help='Path to the pcd directory')
    parser.add_argument('--output_dir', type=str,
                    help='Directory to save results to')
    
    parser.add_argument('--voxel_size', type=float, default=0.1,
                        help='Voxel size to preprocess point cloud')
    args = parser.parse_args()

    main(args)