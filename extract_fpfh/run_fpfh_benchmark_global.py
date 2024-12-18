import os, shutil
from multiprocessing import Pool
from pathlib import Path

PY3="python3"
N_THREADS = 1
BENCHMARK_DIR="/benchmark/point_clouds_registration_benchmark/dataset_voxelgrid_0.1"
RESULTS_DIR="/benchmark/experiments/FPFH/features/voxelgrid_0.1/"

VOXEL_SIZE = 0.1

base_command = ( f'{PY3}' + ' fpfh_benchmark.py' +
                 f' --voxel_size={VOXEL_SIZE}')

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

feature_dirs = ['kaist/urban05/',
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

for problem_txt, pcd_dir, feature_dir in zip(problem_txts, pcd_dirs, feature_dirs):
    full_command = (base_command + 
                    f' --input_txt={BENCHMARK_DIR}/{problem_txt}' +
                    f' --input_pcd_dir={BENCHMARK_DIR}/{pcd_dir}' +
                    f' --output_dir={RESULTS_DIR}/{feature_dir}')

    problem_name = Path(problem_txt).stem
    time_command = f'command time --verbose -o {RESULTS_DIR}/{problem_name}_time.txt ' + full_command
    commands.append(time_command)

shutil.rmtree(RESULTS_DIR, ignore_errors=True)
os.makedirs(RESULTS_DIR)
txt_commands = os.path.join(RESULTS_DIR, "readme.txt")
with open(txt_commands, 'w') as f:
    for item in commands:
        f.write("%s\n" % item)

pool = Pool(N_THREADS)
pool.map(os.system, commands)