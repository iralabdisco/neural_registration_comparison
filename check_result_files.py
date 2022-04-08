import glob, sys, os
import pandas as pd

BENCHMARK_DIR="/neural_comparison/point_clouds_registration_benchmark/"
RESULTS_DIR="/neural_comparison/experiments/3DFeatNet/results_teaser_voxelgrid_0.1/"

def check_file(problem_file, result_file):
    df_problem = pd.read_csv(problem_file, sep=';')
    df_result = pd.read_csv(result_file, sep=';', comment='#')

    if len(df_problem) != len(df_result):
        print("Number of rows not ok")
        return
    if df_result.isnull().values.any():
        print("NaN values in results")
        return
    
    print("OK")

def main():
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


    for problem_txt in problem_txts:
        problem_name = os.path.splitext(os.path.basename(problem_txt))[0]
        result_txt = problem_name + "_result.txt"
        problem_file = os.path.join(BENCHMARK_DIR, problem_txt)
        result_file = os.path.join(RESULTS_DIR, result_txt)
        print("---------------")
        print(result_txt)
        check_file(problem_file, result_file)

if __name__ == '__main__':
    main()