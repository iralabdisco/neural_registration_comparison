import pandas as pd
import numpy as np
import argparse
import os, copy, csv, sys

def compute_stats_from_df (df):
    median_error = np.median(df.final_error)
    q_075 = np.quantile(df.final_error, 0.75)
    q_095 = np.quantile(df.final_error, 0.95)
    mean_error = np.mean(df.final_error)
    std_dev = np.std(df.final_error)

    return median_error, q_075, q_095, mean_error, std_dev

def main(args):
    total_df = pd.DataFrame()
    stats_data = []

    #calculate stats for each sequence
    for f in os.listdir(args.input_dir):
        df = pd.read_csv(os.path.join(args.input_dir, f),
                        sep=';',
                        comment='#')
        total_df = pd.concat([total_df, df])
        sequence_name = os.path.splitext(os.path.basename(f))[0]
        stats = list(compute_stats_from_df(df))
        stats.insert(0, sequence_name)
        stats_data.append(stats)    

    #calculate stats for all problems together
    stats = list(compute_stats_from_df(total_df))
    stats.insert(0, "total")
    stats_data.append(stats) 
    
    stats_columns = ["sequence", "median", "0.75 Q", "0.95 Q", "mean", "std_dev"]
    df_stats = pd.DataFrame(stats_data, columns=stats_columns)
    print(df_stats)

    if(args.output_file is not None):
        df_stats.to_csv(args.output_file, na_rep='NaN')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compute results statistics')
    parser.add_argument('--input_dir', type=str, help='Directory where the result files are located')
    parser.add_argument('--output_file', type=str, help='File where the stats will be saved')
    args = parser.parse_args()
    main(args)