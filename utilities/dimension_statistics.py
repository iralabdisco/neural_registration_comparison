import open3d, glob, sys, numpy

clouds = glob.glob(f"{sys.argv[1]}*.pcd")
points = []

for cloud_name in clouds:
    cloud = open3d.io.read_point_cloud(cloud_name)
    points.append(len(cloud.points))

print(f"Mean number of points: {numpy.mean(points)}")
print(f"Max number of points: {numpy.max(points)}")
print(f"Min number of points: {numpy.min(points)}")
