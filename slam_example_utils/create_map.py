import copy

import open3d as o3d
import pandas as pd
from tqdm import tqdm
import os
import numpy as np

if __name__ == "__main__":
    results_file = "/benchmark/tum_slam_comparison/3DSmoothNet/results/TEASER/pioneer_slam2_problems_result.txt"
    problems_file = "/benchmark/tum_slam_comparison/pioneer_slam2_problems.txt"
    pcd_dir = "/benchmark/tum_slam_comparison/pioneer_slam2"

    df_results = pd.read_csv(results_file,
                     sep=';',
                     comment='#')
    df_problems = pd.read_csv(problems_file,
                     sep=' ',
                     comment='#')

    total_map = o3d.geometry.PointCloud()
    total_matrix = np.eye(4)
    index = 0
    for _, results_row in tqdm(df_results.iterrows(), total=df_results.shape[0]):
        problems_row = df_problems.loc[df_problems['id'] == results_row["id"]]

        source: o3d.geometry.PointCloud = o3d.io.read_point_cloud(os.path.join(pcd_dir, problems_row["source"].values[0]))
        target = o3d.io.read_point_cloud(os.path.join(pcd_dir, problems_row["target"].values[0]))

        transform_str = results_row["transformation"]
        transform = np.fromstring(transform_str, dtype=float, sep=' ').reshape((4, 4))

        partial_map = o3d.geometry.PointCloud()
        partial_map.points.extend(target.points)
        partial_map.colors.extend(target.colors)

        source_partial = copy.deepcopy(source)
        source_partial = source_partial.transform(transform)
        partial_map.points.extend(source_partial.points)
        partial_map.colors.extend(source_partial.colors)
        o3d.io.write_point_cloud(f'test_allineamento/{index}.pcd', partial_map)

        total_matrix = total_matrix @ transform
        source = source.transform(total_matrix)
        total_map.points.extend(source.points)
        total_map.colors.extend(source.colors)

        index += 1

    o3d.io.write_point_cloud(f'test.pcd', total_map)

