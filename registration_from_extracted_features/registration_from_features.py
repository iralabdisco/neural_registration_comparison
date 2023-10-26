import argparse
import copy
import csv
import json
import logging
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
    header = ['id', 'initial_error', 'final_error', 'transformation', 'status_code']
    result_name = problem_name + "_result.txt"
    result_filename = os.path.join(args.output_dir, result_name)
    with open(result_filename, mode='w') as f:
        f.write(header_comment)
        csv_writer = csv.writer(f, delimiter=';')
        csv_writer.writerow(header)

    # load config
    config_file= open(args.config_path)
    config = json.load(config_file)

    # create logger
    os.makedirs('logs', exist_ok=True)
    logname = 'logs/' + problem_name + '.log'
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=logname, level=logging.DEBUG, filemode='w')

    # start solving all problems in .txt
    print(problem_name)

    if args.use_status_txt:
        status_df = pd.read_csv(os.path.join(args.input_features_dir, problem_name + "_status.txt"),
                         sep=';',
                         comment='#')

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
        target_npz_filename = os.path.join(args.input_features_dir, os.path.splitext(target_pcd_filename)[0]) + '.npz'
        source_npz_filename = os.path.join(args.input_features_dir, str(problem_id)) + '.npz'

        if args.use_status_txt and (not os.path.exists(target_npz_filename) or not os.path.exists(source_npz_filename)):
            status_code = status_df.loc[df['id'] == problem_id, 'status_code'].values[0]

            registration_solution = np.eye(4)
            # write results to file
            str_solution = ' '.join(map(str, registration_solution.ravel()))
            results = [problem_id, initial_error, initial_error, str_solution, status_code]
            with open(result_filename, mode='a') as f:
                csv_writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONE, escapechar=' ')
                csv_writer.writerow(results)
            continue

        target_npz = np.load(os.path.join(args.input_features_dir, os.path.splitext(target_pcd_filename)[0]) + '.npz')
        source_npz = np.load(os.path.join(args.input_features_dir, str(problem_id)) + '.npz')
        target_features = target_npz['features']
        source_features = source_npz['features']
        target_xyz = target_npz['xyz_down'].T
        source_xyz = source_npz['xyz_down'].T

        # choose n random points
        if (args.use_random_keypoints == "True"):
            xyz_len = source_xyz.shape[1]
            if xyz_len > args.n_keypoints: 
                indexes = np.random.choice(xyz_len, args.n_keypoints, replace=False)
                source_xyz = source_xyz[:, indexes]
                source_features = source_features[indexes, :]
        
        # find correspondences
        if (args.mutual_filter == "True"):
            mutual_flag = True
        else:
            mutual_flag = False

        corrs_S, corrs_T = correspondence_helpers.find_correspondences(
            source_features, target_features, distance_metric=args.distance, mutual_filter=mutual_flag)

        logging.debug("Solving " + str(problem_id))
        logging.debug("Number of target features: " + str(len(target_features)))
        logging.debug("Number of source features: " + str(len(source_features)))
        logging.debug("Number of correspondences: " + str(len(corrs_T)))
        
        # solve registration depending on the chosen algorithm
        if args.algorithm == "RANSAC":
            registration_solution = RANSAC_benchmark.run_RANSAC_registration(config, source_xyz, target_xyz, corrs_S, corrs_T)
        elif args.algorithm == "FastGlobal":
            registration_solution = FastGlobal_benchmark.run_FastGlobal_registration(config, source_xyz, target_xyz, corrs_S, corrs_T)
        elif args.algorithm == "TEASER":
            registration_solution = TEASER_benchmark.run_TEASER_registration(config, source_xyz, target_xyz, corrs_S, corrs_T)
        else:
            raise NotImplementedError
        
        # calculate final error
        moved_source_pcd.transform(registration_solution)
        final_error = metric.calculate_error(source_pcd, moved_source_pcd)

        # write results to file
        str_solution = ' '.join(map(str, registration_solution.ravel()))
        results = [problem_id, initial_error, final_error, str_solution, 'ok']
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
                        help='Distance metric to find correspondences')
    parser.add_argument('mutual_filter', choices=['True', 'False'],
                        help='Use mutual correspondences')

    # Optional keypoints
    parser.add_argument('--use_random_keypoints', choices=['True', 'False'],
                        help='Use random keypoints from source point cloud')
    parser.add_argument('--n_keypoints', type=int,
                        help='Number of random keypoints')

    # I/O files and dirs
    parser.add_argument('--input_txt', type=str,
                    help='Path to the problem .txt')
    parser.add_argument('--input_pcd_dir', type=str,
                        help='Directory which contains the pcd files')
    parser.add_argument('--input_features_dir', type=str,
                        help='Directory which contains the features')
    parser.add_argument('--output_dir', type=str,
                        help='Directory to save the results to')
    parser.add_argument("--use_status_txt", action="store_true", help="Use status txt to check what happend if some features were not generated")

    args = parser.parse_args()

    main(args)
