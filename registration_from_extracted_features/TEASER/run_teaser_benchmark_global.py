import glob, sys, os
from multiprocessing import Pool

PY3="python3"
BENCHMARK_DIR="/neural_comparison/point_clouds_registration_benchmark/"
FEATURES_DIR="/neural_comparison/experiments/FCGF/features/"
RESULTS_DIR="/root/neural_registration_comparison/results/FCGF/teaser/"

DISTANCE_METRIC="euclidean" #for valid metrics see https://github.com/scikit-learn/scikit-learn/issues/4520#issuecomment-89837739

CBAR2=1
NOISE_BOUND=0.2 #voxel size
ESTIMATE_SCALING= False
ROTATION_ESTIMATION_ALGORITHM='GNC_TLS'
ROTATION_GNC_FACTOR=1.4
ROTATION_MAX_ITERATIONS=100
ROTATION_COST_THRESHOLD=1e-12
ROTATION_TIM_GRAPH='CHAIN'
INLIER_SELECTION_MODE='PMC_EXACT'
KCORE_HEURISTIC_THRESHOLD=0.5

base_command = ( f'{PY3}' + ' teaser_benchmark.py'
                f' --distance_metric={DISTANCE_METRIC}' +
                f' --noise_bound={NOISE_BOUND}' +
                f' --cbar2={CBAR2}' +
                f' --estimate_scaling={ESTIMATE_SCALING}' +
                f' --rotation_estimation_algorithm={ROTATION_ESTIMATION_ALGORITHM}' +
                f' --rotation_gnc_factor={ROTATION_GNC_FACTOR}' +
                f' --rotation_max_iterations={ROTATION_MAX_ITERATIONS}' +
                f' --rotation_cost_threshold={ROTATION_COST_THRESHOLD}' +
                f' --rotation_tim_graph={ROTATION_TIM_GRAPH}' +
                f' --inlier_selection_mode={INLIER_SELECTION_MODE}' +
                f' --kcore_heuristic_threshold={KCORE_HEURISTIC_THRESHOLD}')

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
    full_command = (base_command + 
                    f' --input_txt={BENCHMARK_DIR}/{problem_txt}' +
                    f' --input_pcd_dir={BENCHMARK_DIR}/{pcd_dir}' +
                    f' --input_features_dir={FEATURES_DIR}/{features_dir}' +
                    f' --output_dir={RESULTS_DIR}')
    commands.append(full_command)

pool = Pool(1)
pool.map(os.system, commands)
