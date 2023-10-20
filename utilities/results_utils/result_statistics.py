import pandas as pd
import numpy as np
import argparse
import os

def compute_stats_from_df(df):
    df_final_filtered = df.final_error[df['status_code'] == "ok"]

    oom_errors = len(df[df['status_code'] == 'OOM'])
    runtime_errors = len(df[df['status_code'] == 'runtime_error'])

    if not df_final_filtered.empty:
        median_error = np.median(df.final_error[df['status_code'] == "ok"])
        q_075 = np.quantile(df.final_error[df['status_code'] == "ok"], 0.75)
        q_095 = np.quantile(df.final_error[df['status_code'] == "ok"], 0.95)
        mean_error = np.mean(df.final_error[df['status_code'] == "ok"])
        std_dev = np.std(df.final_error[df['status_code'] == "ok"])
    else:
        median_error = float('nan')
        q_075 = float('nan')
        q_095 = float('nan')
        mean_error = float('nan')
        std_dev = float('nan')

    return median_error, q_075, q_095, mean_error, std_dev, oom_errors, runtime_errors


def get_df(input_dir):
    total_df = pd.DataFrame()
    stats_data = []

    # calculate stats for each sequence
    for f in os.listdir(input_dir):
        if f.endswith("result.txt"):
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
                     "0.75 Q", "0.95 Q", "mean", "std_dev", "oom_errors", "runtime_errors"]
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
    
    folders = ["kitti", "3d-match"]
    stats = ["median","0.75 Q", "0.95 Q"]

    full_stats = pd.DataFrame(sequences, columns=['sequence'])
    full_stats.set_index("sequence", inplace=True)

    all_stats = []
    for folder in folders:
        dir_results = os.path.join(args.input_dir, folder)
        df_stats = get_df(dir_results)
        all_stats.append(df_stats[stats])
        if args.write_csv is True:
            df_stats.to_csv(f"{dir_results}/result_stats.csv", na_rep='NaN')
        
        print(folder)
        print(df_stats[['median', '0.95 Q', 'oom_errors', 'runtime_errors']])
        print("----------")

    full_stats = pd.concat(all_stats, axis=1, keys=[f.split("_")[0] for f in folders])
    print(full_stats)
    print(full_stats.to_latex(float_format="%.2f", bold_rows =  True, caption = os.path.dirname(args.input_dir), multicolumn= True, longtable= False))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compute results statistics')
    parser.add_argument('input_dir', type=str,
                        help='Directory where the result files are located')
    parser.add_argument('--write_csv', type=bool,
                        default = False)
    args = parser.parse_args()
    main(args)
