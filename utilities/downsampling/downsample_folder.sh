#!/bin/bash

cd $1
echo "$PWD"
for file in *.pcd; do
    if [ ${file} != "box_map.pcd" ]
    then
    	pcl_voxel_grid $file $file -leaf $2 $2 $2 >/dev/null;
    fi
done
cd "-" > /dev/null
