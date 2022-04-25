import argparse
import copy
import csv
import logging
import os
import sys

import numpy as np
import open3d as o3d
import pandas as pd
import teaserpp_python
from sklearn.neighbors import KDTree
from tqdm import tqdm

import helpers
import metric


def main(args):
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    df = pd.read_csv(args.input_txt, sep=' ', comment='#')
    df = df.reset_index()

    header_comment = "# " + " ".join(sys.argv[:]) + "\n"
    header = ['id', 'initial_error', 'final_error', 'transformation']

    problem_name = os.path.splitext(os.path.basename(args.input_txt))[0]
    result_name = problem_name + "_result.txt"
    result_filename = os.path.join(args.output_dir, result_name)

    logname = 'logs/' + problem_name + '.log'
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=logname, level=logging.DEBUG, filemode='w')

    with open(result_filename, mode='w') as f:
        f.write(header_comment)
        csv_writer = csv.writer(f, delimiter=';')
        csv_writer.writerow(header)
 
    # Populate teaser parameters
    solver_params = teaserpp_python.RobustRegistrationSolver.Params()
    solver_params.cbar2 = args.cbar2
    solver_params.noise_bound = args.noise_bound
    if (args.estimate_scaling == "True"):
        solver_params.estimate_scaling = True
    else:
        solver_params.estimate_scaling = False
    if (args.rotation_estimation_algorithm == "GNC_TLS"):
        solver_params.rotation_estimation_algorithm = (
            teaserpp_python.RobustRegistrationSolver.ROTATION_ESTIMATION_ALGORITHM.GNC_TLS
        )
    elif (args.rotation_estimation_algorithm == "FGR"):
        solver_params.rotation_estimation_algorithm = (
            teaserpp_python.RobustRegistrationSolver.ROTATION_ESTIMATION_ALGORITHM.FGR
        )
    else:
        raise ValueError('Specified rotation_estimation_algorithm does not exist')

    solver_params.rotation_gnc_factor = args.rotation_gnc_factor
    solver_params.rotation_max_iterations = args.rotation_max_iterations
    solver_params.rotation_cost_threshold = args.rotation_cost_threshold

    if(args.rotation_tim_graph == "CHAIN"):
        solver_params.rotation_tim_graph = (teaserpp_python.RobustRegistrationSolver.INLIER_GRAPH_FORMULATION.CHAIN)
    elif(args.rotation_tim_graph == "COMPLETE"):
        solver_params.rotation_tim_graph = (teaserpp_python.RobustRegistrationSolver.INLIER_GRAPH_FORMULATION.COMPLETE)
    else:
        raise ValueError('Specified rotation_tim_graph does not exist')

    if (args.inlier_selection_mode == "PMC_EXACT"):
        solver_params.inlier_selection_mode = (teaserpp_python.RobustRegistrationSolver.INLIER_SELECTION_MODE.PMC_EXACT)
    elif (args.inlier_selection_mode == "PMC_HEU"):
        solver_params.inlier_selection_mode = (teaserpp_python.RobustRegistrationSolver.INLIER_SELECTION_MODE.PMC_HEU)
    elif (args.inlier_selection_mode == "KCORE_HEU"):
        solver_params.inlier_selection_mode = (teaserpp_python.RobustRegistrationSolver.INLIER_SELECTION_MODE.KCORE_HEU)
    elif (args.inlier_selection_mode == "NONE"):
        solver_params.inlier_selection_mode = (teaserpp_python.RobustRegistrationSolver.INLIER_SELECTION_MODE.NONE)
    else:
        raise ValueError('Specified inlier_selection_mode does not exist')

    solver_params.kcore_heuristic_threshold = args.kcore_heuristic_threshold

    logging.info(solver_params)

    n_problems = len(df.index)

    print(problem_name)
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        problem_id = row['id']

        source_pcd_filename = row['source']
        source_pcd_file = os.path.join(args.input_pcd_dir, source_pcd_filename)
        source_pcd = o3d.io.read_point_cloud(source_pcd_file, remove_nan_points=True, 
                                            remove_infinite_points=True)

        target_pcd_filename = row['target']

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
        target_npz = np.load(os.path.join(args.input_features_dir, os.path.splitext(target_pcd_filename)[0]) + '.npz')
        source_npz = np.load(os.path.join(args.input_features_dir, str(problem_id)) + '.npz')

        target_features = target_npz['features']
        source_features = source_npz['features']
        
        target_xyz = target_npz['xyz_down']
        source_xyz = source_npz['xyz_down']

        corrs_S, corrs_T = helpers.find_correspondences(source_features, target_features)

        S_corr = source_xyz.transpose()[:, corrs_S]
        T_corr = target_xyz.transpose()[:, corrs_T]

        logging.debug("Solving " + str(problem_id))
        logging.debug("Target features file: " + os.path.splitext(target_pcd_filename)[0] + '.csv')
        logging.debug("Source features file: " + str(problem_id) + '.csv')
        logging.debug("Number of target features: " + str(len(target_features)))
        logging.debug("Number of source features: " + str(len(source_features)))
        logging.debug("Target corres: " + str(len(T_corr)))
        logging.debug("Source corres: " + str(len(S_corr)))

        if (len(T_corr) > 1):
            # solve with TEASER++
            logging.debug("Solving with TEASER")
            teaserpp_solver = teaserpp_python.RobustRegistrationSolver(solver_params)

            #teaserpp_solver = helpers.get_teaser_solver(0.1)
            teaserpp_solver.solve(S_corr,T_corr)
            solution = teaserpp_solver.getSolution()

            registration_solution = np.eye(4)       
            registration_solution[0:3, 0:3] = solution.rotation
            registration_solution[:3, 3] = solution.translation
        else:
            logging.debug("Not solving due to insufficient corrispondences")
            registration_solution = np.eye(4)

        moved_source_pcd.transform(registration_solution)
        final_error = metric.calculate_error(source_pcd, moved_source_pcd)

        logging.info("Solved problems: " + str(index + 1) + "/" + str(n_problems))

        # write results to file
        str_solution = ' '.join(map(str, registration_solution.ravel()))
        results = [problem_id, initial_error, final_error, 
                    str_solution]
        with open(result_filename, mode='a') as f:
            csv_writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONE, escapechar=' ')
            csv_writer.writerow(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute benchmark problems')
    parser.add_argument('--gpu', type=int, default=3,
                        help='GPU to use (default: 0)')
    # Input/checkpoint/output paths
    parser.add_argument('--input_txt', type=str,
                        help='Path to the problem .txt')
    parser.add_argument('--input_pcd_dir', type=str,
                        help='Directory which contains the pcd files')
    parser.add_argument('--input_features_dir', type=str,
                        help='Directory which contains the features')
    parser.add_argument('--output_dir', type=str,
                        help='Directory to save the results to')
    # TEASER parameters
    parser.add_argument('--cbar2', type=float,
                        help='TEASER cbar2')
    parser.add_argument('--noise_bound', type=float,
                        help='TEASER noise_bound')
    parser.add_argument('--estimate_scaling', type=str,
                        help='TEASER estimate_scaling')
    parser.add_argument('--rotation_estimation_algorithm', type=str,
                        help='TEASER rotation_estimation_algorithm')
    parser.add_argument('--rotation_gnc_factor', type=float,
                        help='TEASER rotation_gnc_factor')
    parser.add_argument('--rotation_max_iterations', type=int,
                        help='TEASER rotation_max_iterations')
    parser.add_argument('--rotation_cost_threshold', type=float,
                        help='TEASER rotation_cost_threshold')
    parser.add_argument('--rotation_tim_graph', type=str,
                        help='TEASER rotation_tim_graph')
    parser.add_argument('--inlier_selection_mode', type=str,
                        help='TEASER inlier_selection_mode')
    parser.add_argument('--kcore_heuristic_threshold', type=float,
                        help='TEASER kcore_heuristic_threshold')
    parser.add_argument('--distance_metric', type=str,
                        help='Distance metric to use to find correspondences')
    args = parser.parse_args()

    main(args)