import os, shutil
from multiprocessing import Pool

PY3="python3"
BENCHMARK_DIR="/neural_comparison/point_clouds_registration_benchmark"
RESULTS_DIR="/neural_comparison/experiments/FPFH/features_voxelgrid_0.2/"

VOXEL_SIZE = 0.2

base_command = ( f'{PY3}' + ' fpfh_benchmark2.py' +
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
    commands.append(full_command)

shutil.rmtree(RESULTS_DIR, ignore_errors=True)
os.makedirs(RESULTS_DIR)
txt_commands = os.path.join(RESULTS_DIR, "readme.txt")
with open(txt_commands, 'w') as f:
    for item in commands:
        f.write("%s\n" % item)

pool = Pool(1)
pool.map(os.system, commands)