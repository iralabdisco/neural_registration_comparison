import copy
import csv

import open3d as o3d
import pandas as pd
from tqdm import tqdm
import os
import numpy as np


def get_gt_matrix(ground_truth, pcd_name):
    cloud = pcd_name[:-4]
    gt_index = np.abs(ground_truth[:,0] - float(cloud)).argmin()
    T = np.eye(4)

    # quaternion as [w,x,y,z]
    T[:3, :3] = o3d.geometry.get_rotation_matrix_from_quaternion([ground_truth[gt_index, 7],
                                                                  ground_truth[gt_index, 4],
                                                                  ground_truth[gt_index, 5],
                                                                  ground_truth[gt_index, 6]])
    T[0, 3] = ground_truth[gt_index, 1]
    T[1, 3] = ground_truth[gt_index, 2]
    T[2, 3] = ground_truth[gt_index, 3]

    return T


def calculate_error(cloud1: o3d.geometry.PointCloud, cloud2: o3d.geometry.PointCloud) -> float:
    assert len(cloud1.points) == len(cloud2.points), "len(cloud1.points) != len(cloud2.points)"

    centroid, _ = cloud1.compute_mean_and_covariance()
    weights = np.linalg.norm(np.asarray(cloud1.points) - centroid, 2, axis=1)
    distances = np.linalg.norm(np.asarray(cloud1.points) - np.asarray(cloud2.points), 2, axis=1) / len(weights)
    return float(np.sum(distances / weights))


if __name__ == "__main__":
    results_file = "/benchmark/tum_slam_comparison/experiments/OverlapPredator/results/TEASER/pioneer_slam3_problems_result.txt"
    problems_file = "/benchmark/tum_slam_comparison/dataset/pioneer_slam3_problems.txt"
    pcd_dir = "/benchmark/tum_slam_comparison/dataset/pioneer_slam3/"
    gt_file = "/benchmark/tum_slam_comparison/dataset/pioneer_slam3/pioneer_slam3.gt"

    result_folder = "/benchmark/tum_slam_comparison/aligned_pcd/OverlapPredator/pioneer_slam3"

    df_results = pd.read_csv(results_file,
                     sep=';',
                     comment='#')
    df_problems = pd.read_csv(problems_file,
                     sep=' ',
                     comment='#')

    with open(gt_file) as ground_truth_file:
        csv_reader = csv.reader(ground_truth_file, delimiter=' ')
        next(csv_reader)
        next(csv_reader)
        next(csv_reader)
        ground_truth = []
        for row in csv_reader:
            ground_truth.append([float(x) for x in row])
        ground_truth = np.array(ground_truth)

    os.makedirs(result_folder, exist_ok=True)
    errors_list = []
    for _, results_row in tqdm(df_results.iterrows(), total=df_results.shape[0]):
        problems_row = df_problems.loc[df_problems['id'] == results_row["id"]]
        source_filename = problems_row["source"].values[0]
        source: o3d.geometry.PointCloud = o3d.io.read_point_cloud(os.path.join(pcd_dir, source_filename),
                                                                  remove_nan_points=True,
                                                                  remove_infinite_points=True)
        target_filename = problems_row["target"].values[0]
        target = o3d.io.read_point_cloud(os.path.join(pcd_dir, target_filename),
                                         remove_nan_points=True,
                                         remove_infinite_points=True
                                         )

        source.paint_uniform_color([1, 0.706, 0])
        target.paint_uniform_color([0, 0.651, 0.929])

        source_gt = get_gt_matrix(ground_truth, os.path.splitext(source_filename)[0])
        target_gt = get_gt_matrix(ground_truth, os.path.splitext(target_filename)[0])

        transform_str = results_row["transformation"]
        transform = np.fromstring(transform_str, dtype=float, sep=' ').reshape((4, 4))

        target = target.transform(target_gt)
        source_est_t = copy.deepcopy(source)
        source_est_t = source_est_t.transform(target_gt@transform)

        source_gt_t = copy.deepcopy(source)
        source_gt_t = source_gt_t.transform(source_gt)

        partial_map = o3d.geometry.PointCloud()
        partial_map.points.extend(target.points)
        partial_map.colors.extend(target.colors)

        partial_map.points.extend(source_est_t.points)
        partial_map.colors.extend(source_est_t.colors)

        error = calculate_error(source_gt_t, source_est_t)
        errors_list.append(error)

        problem_id = results_row['id']
        o3d.io.write_point_cloud(f'{result_folder}/{problem_id}_{error}.pcd', partial_map)

    median = np.median(errors_list)
    q075 = np.quantile(errors_list, 0.75)
    q095 = np.quantile(errors_list, 0.95)

    print(f'Median of errors: {median} \n',
          f'Q 075: {q075} \n',
          f'Q 0.95: {q095}')
