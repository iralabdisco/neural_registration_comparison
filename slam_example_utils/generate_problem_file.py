import csv, numpy, random, sys, binascii, random
import os


def main():
    dataset_path = "/home/fdila/tum_slam/pioneer_slam2/"

    problem_file = "./pioneer_slam2_problems.txt"

    header = "id source target overlap t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12\n"
    out_file = open(problem_file, 'w+')
    base_id = binascii.crc32(problem_file.encode())
    out_file.write(header)

    file_list = sorted_directory_listing_with_os_listdir(dataset_path)

    identity_transform = ("1 0 0 0 "
                          "0 1 0 0 "
                          "0 0 1 0")

    print(identity_transform)

    i = 0
    while i < len(file_list) - 2:
        source_cloud = file_list[i]
        target_cloud = file_list[i + 1]
        out_file.write(
            str(base_id + i) + " "
            + source_cloud + " "
            + target_cloud + " "
            + str(0) + " "
            + identity_transform
            + "\n"
        )
        i += 1
def sorted_directory_listing_with_os_listdir(directory):
    items = os.listdir(directory)
    sorted_items = sorted(items)
    return sorted_items


if __name__ == '__main__':
    main()
