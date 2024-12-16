import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
from matplotlib import ticker

def get_df(input_dirs, algorithms, sequences):
    data = []  # List to store dataframes for each experiment

    for input_dir, algorithm in zip(input_dirs, algorithms):
        for sequence in sequences:
            if algorithm == 'GeoTransformer' and sequence in ['pioneer_slam', 'pioneer_slam3', 'long_office_household']:
                input_dir = '../results/geotransformer/3d-match'

            print(input_dir)
            f = os.path.join(input_dir, sequence+'_global_result.txt')
            df = pd.read_csv(str(f), sep=';', comment='#')
            final_error_array = df['final_error'].values
            # plt.boxplot(final_error_array)
            # plt.title(algorithm+ " " + sequence)
            # plt.show()

            df = pd.DataFrame({"Algorithm": algorithm, "Sequence": sequence, "Error": final_error_array})
            data.append(df)

    df = pd.concat(data, ignore_index=True)
    return df


def main(args):
    sequences = ["plain", "stairs", "apartment",
                 "hauptgebaude", "wood_autumn", "wood_summer",
                 "gazebo_summer", "gazebo_winter", "box_met",
                 "p2at_met", "pioneer_slam",
                 "pioneer_slam3", "long_office_household",
                 "urban05"]

    algorithms_folders = ['../results/FPFH/results/voxelgrid_0.1/TEASER',
                          '../results/FCGF/3DMatch_voxel_0.1/results/TEASER',
                          '../results/3DSmoothNet/results/voxelgrid_0.1/TEASER',
                          '../results/geotransformer/kitti/',
                          '../results/RoReg/results/3DMatch/']
    algorithms = ['FPFH', 'FCGF', '3DSmoothNet', 'GeoTransformer', 'RoReg']

    df = get_df(algorithms_folders, algorithms, sequences)

    print(df)
    df.reset_index(inplace=True)

    # All sequences
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 8))
    g = sns.boxplot(data=df, x='Sequence', y='Error', hue='Algorithm',
                palette='colorblind', showfliers=True)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Sequence')
    plt.ylabel('Error')
    plt.yscale('log')

    g.set(yscale='log')
    g.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))
    g.grid(axis='y', which='major', color='gray', linewidth=0.3)
    g.grid(axis='y', which='minor', color='gray', linewidth=0.1)

    plt.ylim(top=100)
    plt.legend(title='Algorithm', loc='upper center', bbox_to_anchor=(0.5, 1.15),
               ncol=5)
    plt.tight_layout()
    plt.show()

    sequences_to_plot = ['wood_autumn', 'wood_summer', 'gazebo_summer', 'gazebo_winter', 'pioneer_slam3']
    filtered_df = df[df['Sequence'].isin(sequences_to_plot)]

    sns.set(style="whitegrid", font_scale=2.5)
    sns.set_context("poster")
    plt.figure(figsize=(22, 12))
    plt.gca().spines['left'].set_linewidth(2)  # Adjust the left spine
    plt.gca().spines['bottom'].set_linewidth(2)  # Adjust the bottom spine
    g = sns.boxplot(data=filtered_df, x='Sequence', y='Error', hue='Algorithm', linewidth=2, palette='colorblind')
    plt.xticks(rotation=15, ha='right', fontsize=28)
    plt.yticks(fontsize=25)
    plt.yscale('log')
    plt.xlabel('')
    plt.ylabel('Error', fontsize=33, fontweight=548, labelpad=15)
    legend = plt.legend(title='Algorithm', loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=5, fontsize=29)
    plt.setp(legend.get_title(), fontsize=33, fontweight=548)
    plt.tight_layout()

    g.set(yscale='log')
    g.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))
    g.grid(axis='y', which='major', color='gray', linewidth=0.3)
    g.grid(axis='y', which='minor', color='gray', linewidth=0.1)

    plt.savefig('boxplots_algorithms1.png', dpi=200)
    plt.show()

    sequences_to_plot = ['plain', 'box_met', 'p2at_met', 'pioneer_slam', 'urban05']
    # Filter the melted_df DataFrame to include only the specified sequences
    filtered_df = df[df['Sequence'].isin(sequences_to_plot)]

    sns.set(style="whitegrid", font_scale=2.5)
    sns.set_context("poster")
    plt.figure(figsize=(22, 12))
    g = sns.boxplot(data=filtered_df, x='Sequence', y='Error', hue='Algorithm', palette='colorblind', linewidth=2,
                legend=False)
    plt.xticks(rotation=15, ha='right', fontsize=28)
    plt.yticks(fontsize=25)
    plt.xlabel('Sequence', fontsize=33, fontweight=548, labelpad=35)
    plt.ylabel('Error', fontsize=33, fontweight=548, labelpad=15)
    plt.yscale('log')
    plt.ylim(top=100)
    # plt.legend(title='Algorithm', loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5)

    g.set(yscale='log')
    g.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))
    g.grid(axis='y', which='major', color='gray', linewidth=0.3)
    g.grid(axis='y', which='minor', color='gray', linewidth=0.1)

    plt.tight_layout()
    plt.savefig('boxplots_algorithms2.png', dpi=200)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute results statistics')
    args = parser.parse_args()
    main(args)
