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
        initial_error = np.median(df.initial_error[df['status_code'] == "ok"])
        residual = np.median((df.final_error[df['status_code'] == "ok"])/(df.initial_error[df['status_code'] == "ok"])*100)
    else:
        median_error = float('nan')
        initial_error = float('nan')
        residual = float('nan')

    return median_error, initial_error, residual, oom_errors, runtime_errors


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
                     "initial_error", "residual","oom_errors", "runtime_errors"]
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
    
    #folders = [name for name in os.listdir(args.input_dir) if os.path.isdir(args.input_dir + "/" + name)]
    stats = ["median", "initial_error", "residual"]

    full_stats = pd.DataFrame(sequences, columns=['sequence'])
    full_stats.set_index("sequence", inplace=True)

    all_stats = []
    errors_stats = []

    dir_results = args.input_dir
    df_stats = get_df(dir_results)
    all_stats.append(df_stats[stats])
        
    if len(errors_stats) == 0:
        errors_stats.append(df_stats[["oom_errors", "runtime_errors"]])
        print(df_stats[['oom_errors', 'runtime_errors']])
    if args.write_csv is True:
        df_stats.to_csv(f"{dir_results}/result_stats.csv", na_rep='NaN')
    print("----------")
    full_stats = pd.concat(all_stats, axis=1, keys=[dir_results])
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
