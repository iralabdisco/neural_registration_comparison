import argparse
import os

import numpy as np
import pandas as pd
from tqdm import tqdm


def main(args):
    datasets = ['eth', 'tum', 'kaist', 'planetary']
    dataset_dirs = []
    for dataset in datasets:
        full_dir = os.path.join(args.input_dir, dataset)
        dataset_dirs.append(full_dir)

    for dataset in dataset_dirs:
        for dirpath, dirnames, filenames in os.walk(dataset):
            if not dirnames:
                path = os.path.normpath(dirpath)
                relative_path = os.path.relpath(path, args.input_dir)
                new_dir = os.path.join(args.output_dir, relative_path)
                os.makedirs(new_dir, exist_ok=True)
                for file in tqdm(filenames):
                    csv_file = os.path.join(dirpath, file)
                    filename = os.path.splitext(file)[0]
                    npz_file = os.path.join(new_dir, filename)
                    df = pd.read_csv(csv_file, comment='#')
                    features = df.loc[:, df.columns.difference(['x','y','z'])].to_numpy()        
                    xyz_down = df[['x', 'y', 'z']].to_numpy()
                    np.savez_compressed(npz_file, xyz_down=xyz_down.T, features=features)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert csv to npz')
    parser.add_argument('input_dir', type=str, help='Directory where the csv files are located')
    parser.add_argument('output_dir', type=str, help='Directory where the npz files will be saved')
    args = parser.parse_args()
    main(args)
