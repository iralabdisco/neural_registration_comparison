import pandas as pd
import numpy as np
import argparse
import os
import copy
import csv
import sys


def compute_stats_from_df(df):
    median_error = np.median(df.final_error)
    q_075 = np.quantile(df.final_error, 0.75)
    q_095 = np.quantile(df.final_error, 0.95)
    mean_error = np.mean(df.final_error)
    std_dev = np.std(df.final_error)

    return median_error, q_075, q_095, mean_error, std_dev


def get_df(input_dir):
    total_df = pd.DataFrame()
    stats_data = []

    # calculate stats for each sequence
    for f in os.listdir(input_dir):
        if f.endswith(".txt"):
            df = pd.read_csv(os.path.join(input_dir, f),
                             sep=';',
                             comment='#')
            total_df = pd.concat([total_df, df])
            sequence_name = os.path.splitext(os.path.basename(f))[0]
            sequence_name = sequence_name.split("_")
            sequence_name = "_".join(sequence_name[:-2])
            stats = list(compute_stats_from_df(df))
            stats.insert(0, sequence_name)
            stats_data.append(stats)

    # calculate stats for all problems together
    stats = list(compute_stats_from_df(total_df))
    stats.insert(0, "Total")
    stats_data.append(stats)

    stats_columns = ["sequence", "median",
                     "0.75 Q", "0.95 Q", "mean", "std_dev"]
    df_stats = pd.DataFrame(stats_data, columns=stats_columns)

    df_stats['sequence'] = pd.Categorical(df_stats['sequence'], ["plain", "stairs", "apartment",
                                                                 "hauptgebaude", "wood_autumn", "wood_summer",
                                                                 "gazebo_summer", "gazebo_winter", "box_met",
                                                                 "p2at_met", "planetary_map", "pioneer_slam",
                                                                 "pioneer_slam3", "long_office_household",
                                                                 "urban05", "Total"])

    df_stats.set_index("sequence", inplace=True)
    df_stats = df_stats.sort_values("sequence")

    return df_stats


def main(args):
    sequences = ["plain", "stairs", "apartment",
                 "hauptgebaude", "wood_autumn", "wood_summer",
                 "gazebo_summer", "gazebo_winter", "box_met",
                 "p2at_met", "planetary_map", "pioneer_slam",
                 "pioneer_slam3", "long_office_household",
                 "urban05", "Total"]
    
    folders = ["RANSAC_voxelgrid_0.2", "FastGlobal_voxelgrid_0.2", "TEASER_voxelgrid_0.2"]
    stats = ["median","0.75 Q", "0.95 Q"]
    multi_columns = ["sequence"] + [(f.split("_")[0],s) for f,s in zip(folders, stats)]
    
    full_stats = pd.DataFrame(sequences, columns=['sequence'])
    full_stats.set_index("sequence", inplace=True)


    all_stats = []
    for folder in folders:
        dir = os.path.join(args.input_dir, folder)
        df_stats = get_df(dir)
        all_stats.append(df_stats[stats])
        #print(df_stats.rename({"median":f"median_{folder}"}, axis = 1))
        #renamed = df_stats.rename({"median":f"median_{folder}"}, axis = 1)[f"median_{folder}"]
        
        #renamed = df_stats.add_suffix(f"_{folder}")
        #full_stats = full_stats.join(renamed, on="sequence")

        # print(df_stats.reset_index().to_string(index=False))
        #print(df_stats.to_latex(columns = ["median", "0.75 Q", "0.95 Q"], float_format="%.2f", bold_rows =  True))
        if (args.write_csv is True):
            df_stats.to_csv(f"{dir}/result_stats.csv", na_rep='NaN')
        
        print(folder)
        print(df_stats)
        print("----------")


    full_stats = pd.concat(all_stats, axis=1, keys=[f.split("_")[0] for f in folders])
    print(full_stats)
    #medians = full_stats.columns.str.contains('median*')
    print(full_stats.to_latex(float_format="%.2f", bold_rows =  True, caption = os.path.dirname(args.input_dir), multicolumn= True, longtable= False))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compute results statistics')
    parser.add_argument('input_dir', type=str,
                        help='Directory where the result files are located')
    parser.add_argument('--write_csv', type=bool,
                        default = False)
    args = parser.parse_args()
    main(args)
