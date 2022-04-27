import os
import shutil
from multiprocessing import Pool

PY3="python3"
BENCHMARK_DIR="/neural_comparison/point_clouds_registration_benchmark/"
FEATURES_DIR="/neural_comparison/experiments/FPFH/features_voxelgrid_0.2/"
RESULTS_DIR="/root/neural_registration_comparison/results/FPFH/fgr/"

DISTANCE_METRIC="euclidean" #for valid metrics see https://github.com/scikit-learn/scikit-learn/issues/4520#issuecomment-89837739

VOXEL_SIZE = 0.2

DECREASE_MU = "True"
DIVISION_FACTOR = 1.4
ITERATION_NUMBER = 150
MAXIMUM_CORRESPONDENCE_DISTANCE = VOXEL_SIZE * 0.5
MAXIMUM_TUPLE_COUNT = 1000
TUPLE_SCALE = 0.95
TUPLE_TEST = "True"
USE_ABSOLUTE_SCALE = "False"

fgr_command = ( f'{PY3}' + ' fast_global_benchmark.py'
                f' --distance_metric={DISTANCE_METRIC}' +
                f' --decrease_mu={DECREASE_MU}' +
                f' --division_factor={DIVISION_FACTOR}' +
                f' --iteration_number={ITERATION_NUMBER}' +
                f' --maximum_correspondence_distance={MAXIMUM_CORRESPONDENCE_DISTANCE}' +
                f' --maximum_tuple_count={MAXIMUM_TUPLE_COUNT}' +
                f' --tuple_scale={TUPLE_SCALE}' +
                f' --tuple_test={TUPLE_TEST}' +
                f' --use_absolute_scale={USE_ABSOLUTE_SCALE}')

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
    full_command = (fgr_command + 
                    f' --input_txt={BENCHMARK_DIR}/{problem_txt}' +
                    f' --input_pcd_dir={BENCHMARK_DIR}/{pcd_dir}' +
                    f' --input_features_dir={FEATURES_DIR}/{features_dir}' +
                    f' --output_dir={RESULTS_DIR}')
    commands.append(full_command)

shutil.rmtree(RESULTS_DIR, ignore_errors=True)
os.makedirs(RESULTS_DIR)
pool = Pool(1)
pool.map(os.system, commands)
