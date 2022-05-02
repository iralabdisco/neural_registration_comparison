import os
import shutil
from multiprocessing import Pool

PY3="python3"
N_THREADS = 1

"""
Nota per i file config.json:

Per RANSAC settare "max_correspondence_distance" a VOXEL_SIZE * 1.5
Per Fast Global Registration settare "maximum_correspondence_distance" a VOXEL_SIZE*0.5
Per TEASER settare "noise_bound" a VOXEL_SIZE
"""
ALGORITHM = "TEASER"
CONFIG = "TEASER_config.json"
DISTANCE = "l2"
MUTUAL_FILTER = "True"
USE_RANDOM_KEYPOINTS = "True"
N_KEYPOINTS = 5000

BENCHMARK_DIR="/neural_comparison/point_clouds_registration_benchmark/"
FEATURES_DIR="/neural_comparison/experiments/FCGF/all_kitti/"
RESULTS_DIR="/root/neural_registration_comparison/results/FCGF/all_kitti/TEASER"


base_command = ( f'{PY3}' + ' registration_from_features.py'
                f' {ALGORITHM}' +
                f' {CONFIG}' +
                f' {DISTANCE}' +
                f' {MUTUAL_FILTER}' +
                f' --use_random_keypoints={USE_RANDOM_KEYPOINTS}' +
                f' --n_keypoints={N_KEYPOINTS}')

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

# delete and recreate result directory
shutil.rmtree(RESULTS_DIR, ignore_errors=True)
os.makedirs(RESULTS_DIR)
# save config in result directory
shutil.copyfile(CONFIG, os.path.join(RESULTS_DIR, CONFIG))

pool = Pool(N_THREADS)
pool.map(os.system, commands)