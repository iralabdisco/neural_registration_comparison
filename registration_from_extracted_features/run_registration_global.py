import os
import shutil
from multiprocessing import Pool
from pathlib import Path
import json

PY3="python3"
N_THREADS = 1

ALGORITHM = "RANSAC"
CONFIG = f"{ALGORITHM}_config.json"
DISTANCE = "euclidean"
MUTUAL_FILTER = "True"
USE_RANDOM_KEYPOINTS = "True"
N_KEYPOINTS = 5000
VOXEL_SIZE = 0.1
USE_STATUS_TXT = True

BENCHMARK_DIR="/benchmark/point_clouds_registration_benchmark/"
FEATURES_DIR="/benchmark/experiments/OverlapPredator/KITTI/features"
RESULTS_DIR=f"/benchmark/experiments/OverlapPredator/KITTI/results/{ALGORITHM}/"

base_command = ( f'{PY3}' + ' registration_from_features.py'
                f' {ALGORITHM}' +
                f' {CONFIG}' +
                f' {DISTANCE}' +
                f' {MUTUAL_FILTER}' +
                f' --use_random_keypoints={USE_RANDOM_KEYPOINTS}' +
                f' --n_keypoints={N_KEYPOINTS}')
if USE_STATUS_TXT:
    base_command = base_command + " --use_status_txt"

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

#Update registration parameters based on voxel size
with open(CONFIG) as config_file:
    config = json.load(config_file)
    if ALGORITHM == "RANSAC":
        config["max_correspondence_distance"] = VOXEL_SIZE*1.5
    elif ALGORITHM == "TEASER":
        config["noise_bound"] = VOXEL_SIZE
    elif ALGORITHM == "FastGlobal":
        config["maximum_correspondence_distance"] = VOXEL_SIZE*0.5
    else:
        raise NotImplemented
with open(CONFIG, 'w') as config_file:
    json.dump(config, config_file)

for problem_txt, pcd_dir, features_dir in zip(problem_txts, pcd_dirs, features_dirs):
    full_command = (base_command + 
                    f' --input_txt={BENCHMARK_DIR}/{problem_txt}' +
                    f' --input_pcd_dir={BENCHMARK_DIR}/{pcd_dir}' +
                    f' --input_features_dir={FEATURES_DIR}/{features_dir}' +
                    f' --output_dir={RESULTS_DIR}')

    problem_name = Path(problem_txt).stem
    time_command = f'command time --verbose -o {RESULTS_DIR}/{problem_name}_time.txt ' + full_command
    commands.append(time_command)

# delete and recreate result directory
answer = input(f"Delete previous {RESULTS_DIR} experiments? [Y/N] ")
if answer != "Y":
    print("Quitting...")
    exit()

shutil.rmtree(RESULTS_DIR, ignore_errors=True)
os.makedirs(RESULTS_DIR)
# save config in result directory
shutil.copyfile(CONFIG, os.path.join(RESULTS_DIR, CONFIG))

pool = Pool(N_THREADS)
pool.map(os.system, commands)