import os
import argparse

import numpy as np
from tqdm import tqdm
import pandas as pd
import open3d as o3d

import benchmark_helper

def extract_features(pcd, voxel_size):
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh

def main():
    parser = argparse.ArgumentParser(description='Point Cloud Registration')
    
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
    os.makedirs(args.output_dir, exist_ok=True)

    ## Load problems txt file
    df = pd.read_csv(args.input_txt, sep=' ', comment='#')
    df = df.reset_index()

    print("Solving: " + args.input_txt)
    num_processed = 0
    ## Solve for each problem
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        problem_id, source_pcd, target_pcd, source_transform, target_pcd_filename = \
                         benchmark_helper.load_problem(row, args)

        ## Extract features from source
        source_features_npz = os.path.join(args.output_dir, '{}'.format(problem_id))
        source_pcd.transform(source_transform)
        xyz_down, features = extract_features(source_pcd, args.voxel_size)

        # Save out the output
        np.savez_compressed(source_features_npz, xyz_down=np.asarray(xyz_down.points), features=features.data.transpose())  

        ## Extract features from target
        target_features_npz = os.path.join(args.output_dir, os.path.splitext(target_pcd_filename)[0])
        if not(os.path.isfile(target_features_npz + '.npz')):     
            xyz_down, features = extract_features(target_pcd, args.voxel_size)

        # Save out the output
        np.savez_compressed(target_features_npz, xyz_down=np.asarray(xyz_down.points), features=features.data.transpose())  
                
if __name__ == '__main__':
    main()