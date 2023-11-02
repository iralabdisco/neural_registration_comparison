import pandas as pd
import argparse
import os

def get_number_of_executions(benchmark_dir, sequence, features):
    txt_name = os.path.join(benchmark_dir, sequence+"_global.txt")
    df = pd.read_csv(txt_name, sep=' ', comment='#')
    df = df.reset_index()
    if features:
        #only count unique target pc since we only calculate the features once
        source_pc_number = len(df)
        target_pc_number = df['target'].nunique()
        executions = source_pc_number + target_pc_number
        pass
    else:
        executions = len(df)

    return executions

def time_to_seconds(time_str):
    # Split the time string into components
    components = time_str.split(':')
    if len(components) == 3:  # Format: "h:mm:ss"
        hours, minutes, seconds = map(float, components)
        total_seconds = hours * 3600 + minutes * 60 + seconds
    elif len(components) == 2:  # Format: "m:ss"
        minutes, seconds = map(float, components)
        total_seconds = minutes * 60 + seconds
    else:
        raise ValueError("Invalid time format")

    return total_seconds

def get_times(input_dir):
    stats_data = []
    total_time = 0
    total_executions = 0
    # calculate stats for each sequence
    for f in os.listdir(input_dir):
        if f.endswith("time.txt"):
            sequence_name = os.path.splitext(os.path.basename(f))[0]
            sequence_name = sequence_name.split("_")
            sequence_name = "_".join(sequence_name[:-2])

            n_executions = get_number_of_executions(args.benchmark_dir, sequence_name, args.features)
            total_executions += n_executions
            with open(os.path.join(input_dir, f), 'r') as file:
                # Read the file line by line
                lines = file.readlines()
                for i, string in enumerate(lines):
                    if string.startswith("\tElapsed (wall clock) time"):
                        index = i
                        break
                time_line = lines[index]

            time = time_line.split()[-1]
            time_seconds = time_to_seconds(time)

            time_per_execution = time_seconds/n_executions
            stats = [time_seconds, time_per_execution]
            stats.insert(0, sequence_name)
            stats_data.append(stats)
            total_time += time_seconds

    # calculate stats for all problems together
    stats = [total_time, total_time/total_executions]
    stats.insert(0, "Total")
    stats_data.append(stats)

    stats_columns = ["sequence", "total time [s]", "avg time [s]"]
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


    dir = os.path.join(args.input_dir)
    df_stats = get_times(dir)
    if args.write_csv is True:
        df_stats.to_csv(f"{dir}/result_stats.csv", na_rep='NaN')

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df_stats)
    print("----------")

    print(df_stats.to_latex(float_format="%.2f", bold_rows=True, caption=os.path.dirname(args.input_dir),
                              multicolumn=True, longtable=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute results statistics')
    parser.add_argument('input_dir', type=str,
                        help='Directory where the result files are located')
    parser.add_argument('benchmark_dir', type=str, help='Benchmark txt problems location', nargs='?',
                        default="/benchmark/point_clouds_registration_benchmark/devel/registration_pairs/")
    parser.add_argument('--write_csv', type=bool,
                        default=False)
    parser.add_argument('--features', action='store_true', default=False)
    args = parser.parse_args()
    main(args)
