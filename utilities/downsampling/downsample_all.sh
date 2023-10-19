#!/bin/bash
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
    ls
    command time -v -o $line"/time.txt" bash ../downsample_folder.sh $line $1
done