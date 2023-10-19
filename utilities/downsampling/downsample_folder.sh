#!/bin/bash

cd $1
echo "$PWD"
for file in *.pcd; do pcl_voxel_grid $file $file -leaf $2 $2 $2 >/dev/null;done
cd "-" > /dev/null