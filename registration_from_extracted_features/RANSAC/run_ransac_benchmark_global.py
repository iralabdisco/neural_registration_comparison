import os
from multiprocessing import Pool

def main():
    PY3="python3"
    BENCHMARK_DIR="/neural_comparison/point_clouds_registration_benchmark/"
    FEATURES_DIR="/neural_comparison/experiments/FPFH/features_voxelgrid_0.2/"
    RESULTS_DIR="/root/neural_registration_comparison/results/FPFH/ransac/"

    DISTANCE_METRIC="euclidean" #for valid metrics see https://github.com/scikit-learn/scikit-learn/issues/4520#issuecomment-89837739

    VOXEL_SIZE = 0.2

    MAX_CORRESPONDENCE_DISTANCE = VOXEL_SIZE * 1.5
    ESTIMATION_METHOD = "TransformationEstimationPointToPoint"
    RANSAC_N = 3
    RANSAC_CONFIDENCE = 0.999
    RANSAC_MAX_ITERATION = 100000

    ransac_command = ( f'{PY3}' + ' ransac_benchmark.py'
                    f' --distance_metric={DISTANCE_METRIC}' +
                    f' --max_correspondence_distance={MAX_CORRESPONDENCE_DISTANCE}' +
                    f' --estimation_method={ESTIMATION_METHOD}' +
                    f' --ransac_n={RANSAC_N}' +
                    f' --ransac_confidence={RANSAC_CONFIDENCE}' +
                    f' --ransac_max_iteration={RANSAC_MAX_ITERATION}')

    problem_txts = ['kaist/urban05_global.txt',
                    'eth/apartment_global.txt', 
                    'eth/gazebo_summer_global.txt',
                    'eth/gazebo_winter_global.txt',
                    'eth/hauptgebaude_global.txt',
                    'eth/plain_global.txt',
                    'eth/stairs_global.txt',
                    'eth/wood_autumn_global.txt',
                    'eth/wood_summer_global.txt',
                    'tum/long_office_household_global.txt',
                    'tum/pioneer_slam_global.txt',
                    'tum/pioneer_slam3_global.txt',
                    'planetary/box_met_global.txt',
                    'planetary/p2at_met_global.txt',
                    'planetary/planetary_map_global.txt']

    pcd_dirs = ['kaist/urban05/',
                'eth/apartment/', 
                'eth/gazebo_summer/',
                'eth/gazebo_winter/',
                'eth/hauptgebaude/',
                'eth/plain/',
                'eth/stairs/',
                'eth/wood_autumn/',
                'eth/wood_summer/',
                'tum/long_office_household/',
                'tum/pioneer_slam/',
                'tum/pioneer_slam3/',
                'planetary/box_met/',
                'planetary/p2at_met/',
                'planetary/p2at_met/']

    features_dirs = ['kaist/urban05/',
                    'eth/apartment/', 
                    'eth/gazebo_summer/',
                    'eth/gazebo_winter/',
                    'eth/hauptgebaude/',
                    'eth/plain/',
                    'eth/stairs/',
                    'eth/wood_autumn/',
                    'eth/wood_summer/',
                    'tum/long_office_household/',
                    'tum/pioneer_slam/',
                    'tum/pioneer_slam3/',
                    'planetary/box_met/',
                    'planetary/p2at_met/',
                    'planetary/planetary_map/']

    commands = []

    for problem_txt, pcd_dir, features_dir in zip(problem_txts, pcd_dirs, features_dirs):
        full_command = (ransac_command + 
                        f' --input_txt={BENCHMARK_DIR}/{problem_txt}' +
                        f' --input_pcd_dir={BENCHMARK_DIR}/{pcd_dir}' +
                        f' --input_features_dir={FEATURES_DIR}/{features_dir}' +
                        f' --output_dir={RESULTS_DIR}/')
        commands.append(full_command)
    
    pool = Pool(1)
    try:
        pool.map_async(os.system, commands)
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()

if __name__ == '__main__':
    main()