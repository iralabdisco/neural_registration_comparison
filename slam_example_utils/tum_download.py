import os, requests

if __name__ == "__main__":

    datasets = [["pioneer_slam2",
                 "https://vision.in.tum.de/rgbd/dataset/freiburg2/rgbd_dataset_freiburg2_pioneer_slam2-2hz-with"
                 "-pointclouds.bag"]]

    base_dir = "/home/tum/"

    for dataset in datasets:
        try:
            os.mkdir(base_dir + dataset[0])
            os.chdir(base_dir + dataset[0])
        except OSError:
            print("Creation of the directory %s failed" % dataset[0])
            exit()
        else:
            print("Downloading dataset %s" % dataset[0])
        req = requests.get(dataset[1])
        bag_name = dataset[0] + ".bag"
        with open(bag_name, "wb") as archive:
            archive.write(req.content)
            print("Converting from .bag to .pcd")
            os.system(
                "rosbag filter " + bag_name + " filtered_" + bag_name + "\"topic == '/camera/rgb/points' and "
                                                                        "m.fields[3].name == 'rgb'\"")
            os.system("rosrun pcl_ros bag_to_pcd filtered_" + bag_name + " /camera/rgb/points .")
        os.system("for file in ./*.pcd; do pcl_convert_pcd_ascii_binary $file $file 0; done")
        os.system("rm *.bag")

