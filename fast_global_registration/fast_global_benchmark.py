import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree
import open3d as o3d

import argparse
import os, copy, csv, sys

import metric
import helpers

parser = argparse.ArgumentParser(description='Compute benchmark problems')
# Input/checkpoint/output paths
parser.add_argument('--input_txt', type=str,
                    help='Path to the problem .txt')
parser.add_argument('--input_pcd_dir', type=str,
                    help='Directory which contains the pcd files')
parser.add_argument('--input_features_dir', type=str,
                    help='Directory which contains the features')
parser.add_argument('--output_dir', type=str,
                    help='Directory to save the results to')
# Feature matching parameters
parser.add_argument('--distance_metric', type=str,
                    help='Distance metric to use to find correspondences')

args = parser.parse_args()

def main():
    os.makedirs(args.output_dir, exist_ok=True) 

    df = pd.read_csv(args.input_txt, sep=' ', comment='#')
    df = df.reset_index()

    header_comment = "# " + " ".join(sys.argv[:]) + "\n"
    header = ['id', 'initial_error', 'final_error', 'flops', 'transformation']
    result_filename = os.path.join(args.output_dir, os.path.basename(args.input_txt))

    with open(result_filename, mode='w') as f:
        f.write(header_comment)
        csv_writer = csv.writer(f, delimiter=';')
        csv_writer.writerow(header)

    for index, row in df.iterrows():
        problem_id = row['id']

        source_pcd_filename = row['source']
        source_pcd_file = os.path.join(args.input_pcd_dir, source_pcd_filename)
        source_pcd = o3d.io.read_point_cloud(source_pcd_file)

        target_pcd_filename = row['target']
        target_pcd_file = os.path.join(args.input_pcd_dir, target_pcd_filename)
        target_pcd = o3d.io.read_point_cloud(target_pcd_file)

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
        initial_error = metric.calculate_error(source_pcd, moved_source_pcd)
        
        # find correspondences between target and source features
        target_df = pd.read_csv(os.path.join(args.input_features_dir, os.path.splitext(target_pcd_filename)[0] + '.csv'), comment='#')
        source_df = pd.read_csv(os.path.join(args.input_features_dir, str(problem_id) + '.csv'), comment='#')

        target_features = target_df.loc[:, target_df.columns.difference(['x','y','z'])].to_numpy()
        source_features = source_df.loc[:, source_df.columns.difference(['x','y','z'])].to_numpy()
        
        target_xyz = target_df[['x', 'y', 'z']].to_numpy()
        source_xyz = source_df[['x', 'y', 'z']].to_numpy()

        corrs_T, corrs_S = helpers.find_correspondences(
            target_features, source_features, distance_metric=args.distance_metric, mutual_filter=True)

        # solve with FGR

        print("SOLVING " + str(problem_id))

        corres_list = np.array([corrs_S, corrs_T], dtype="int32").transpose()
        corres = o3d.utility.Vector2iVector(corres_list)
        
        source_xyz = o3d.utility.Vector3dVector(source_xyz)
        source_xyz = o3d.geometry.PointCloud(source_xyz)
        target_xyz = o3d.utility.Vector3dVector(target_xyz)
        target_xyz = o3d.geometry.PointCloud(target_xyz)

        result_fast = o3d.pipelines.registration.registration_fgr_based_on_correspondence(
            source_xyz, target_xyz, corres)

        registration_solution = result_fast.transformation        

        registered_source_pcd = copy.deepcopy(source_pcd)
        registered_source_pcd.transform(registration_solution)
        final_error = metric.calculate_error(source_pcd, registered_source_pcd)

        # write results to file
        str_solution = ' '.join(map(str, registration_solution.ravel()))
        results = [problem_id, initial_error, final_error, 
                    str_solution]
        with open(result_filename, mode='a') as f:
            csv_writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONE, escapechar=' ')
            csv_writer.writerow(results)

if __name__ == '__main__':
    main()