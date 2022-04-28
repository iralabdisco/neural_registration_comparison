import argparse
import copy
import csv
import json
import os
import sys

import numpy as np
import open3d as o3d
import pandas as pd
from tqdm import tqdm

import benchmark_helpers
import correspondence_helpers
import metric
import RANSAC_benchmark
import FastGlobal_benchmark
import TEASER_benchmark


def main(args):

    # read problem file
    df = pd.read_csv(args.input_txt, sep=' ', comment='#')
    df = df.reset_index()
    problem_name = os.path.splitext(os.path.basename(args.input_txt))[0]

    # initialize result file
    os.makedirs(args.output_dir, exist_ok=True)
    header_comment = "# " + " ".join(sys.argv[:]) + "\n"
    header = ['id', 'initial_error', 'final_error', 'transformation']
    result_name = problem_name + "_result.txt"
    result_filename = os.path.join(args.output_dir, result_name)
    with open(result_filename, mode='w') as f:
        f.write(header_comment)
        csv_writer = csv.writer(f, delimiter=';')
        csv_writer.writerow(header)

    # load config
    config_file= open(args.config_path)
    config = json.load(config_file)

    # start solving all problems in .txt
    print(problem_name)
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):

        problem_id, source_pcd_filename, target_pcd_filename, source_transform = \
            benchmark_helpers.parse_benchmark_row(row)
        
        source_pcd_file = os.path.join(args.input_pcd_dir, source_pcd_filename)
        source_pcd = o3d.io.read_point_cloud(source_pcd_file, remove_nan_points=True, 
                                            remove_infinite_points=True)

        # calculate initial error
        moved_source_pcd = copy.deepcopy(source_pcd)
        moved_source_pcd.transform(source_transform)
        initial_error = metric.calculate_error(source_pcd, moved_source_pcd)
        
        # load target and source xyz and features
        target_npz = np.load(os.path.join(args.input_features_dir, os.path.splitext(target_pcd_filename)[0]) + '.npz')
        source_npz = np.load(os.path.join(args.input_features_dir, str(problem_id)) + '.npz')
        target_features = target_npz['features']
        source_features = source_npz['features']
        target_xyz = target_npz['xyz_down']
        source_xyz = source_npz['xyz_down']

        # find correspondences
        corrs_T, corrs_S = correspondence_helpers.find_correspondences(
            target_features, source_features, distance_metric=args.distance, mutual_filter=True)
        
        # solve registration depending on the chosen algorithm
        if args.algorithm == "RANSAC":
            registration_solution = RANSAC_benchmark.run_RANSAC_registration(config, source_xyz, target_xyz, corrs_S, corrs_T)
        elif args.algorithm == "FastGlobal":
            registration_solution = FastGlobal_benchmark.run_FastGlobal_registration(config, source_xyz, target_xyz, corrs_S, corrs_T)
        elif args.algorithm == "TEASER":
            registration_solution = TEASER_benchmark.run_TEASER_registration(config, source_xyz, target_xyz, corrs_S, corrs_T)
        
        # calculate final error
        moved_source_pcd.transform(registration_solution)
        final_error = metric.calculate_error(source_pcd, moved_source_pcd)

        # write results to file
        str_solution = ' '.join(map(str, registration_solution.ravel()))
        results = [problem_id, initial_error, final_error, 
                    str_solution]
        with open(result_filename, mode='a') as f:
            csv_writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONE, escapechar=' ')
            csv_writer.writerow(results)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compute benchmark problems')

    # Registration algorithm
    parser.add_argument('algorithm', choices=['RANSAC', 'FastGlobal', 'TEASER'],
                        help='Registration algorithm')
    parser.add_argument('config_path', type=str,
                        help='Algorithm configuration')

    # Distance metric to find correspondences
    parser.add_argument('distance', choices=['chebyshev', 'euclidean', 'cityblock', 'manhattan', 'infinity', 'minkowski', 'p', 'l2', 'l1'],
                        help='Registration algorithm')

    # I/O files and dirs
    parser.add_argument('--input_txt', type=str,
                    help='Path to the problem .txt')
    parser.add_argument('--input_pcd_dir', type=str,
                        help='Directory which contains the pcd files')
    parser.add_argument('--input_features_dir', type=str,
                        help='Directory which contains the features')
    parser.add_argument('--output_dir', type=str,
                        help='Directory to save the results to')

    args = parser.parse_args()

    main(args)
