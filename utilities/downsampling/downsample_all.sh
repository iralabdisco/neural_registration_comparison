#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "Usage: downsample_all.sh VOXEL_LEAF"
    exit 1
fi


echo "Using voxel with leaf $1"

echo "Copying datasets..."
mkdir "dataset_voxelgrid_$1"
cp -r eth "dataset_voxelgrid_$1"
cp -r kaist "dataset_voxelgrid_$1"
cp -r tum "dataset_voxelgrid_$1"
cp -r planetary "dataset_voxelgrid_$1"

cd "dataset_voxelgrid_$1"

echo "Voxel grid downsampling..."
find . -type d -links 2 | while read line; do
    base_name=$(basename ${line})
    time_file=$(realpath --no-symlinks "./"$base_name"_downsampling_time.txt")
    command time -v -o $time_file bash ../downsample_folder.sh $line $1
    if [ ${line} == "./planetary/p2at_met" ]
    then
        command time -v -o "./box_map_downsampling_time.txt" pcl_voxel_grid "./planetary/p2at_met/box_map.pcd" "./planetary/p2at_met/box_map.pcd" -leaf $1 $1 $1 >/dev/null;
    fi
done
