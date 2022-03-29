#ifndef COMPARISON_UTILITY_UNIT_TEST
#define COMPARISON_UTILITY_UNIT_TEST

#include <string>
#include <Eigen/Core>
#include <pcl/io/pcd_io.h>
#include <pcl/filters/filter.h>
#include <gtest/gtest.h>

#include "pcd_utils.hpp"

namespace
{

  TEST(ReadPCD, ReadPCDTest)
  {
    std::string pointcloud_filename("test.pcd");
    std::vector<float> pts;
    int n_points = read_pcd(pointcloud_filename, pts);

    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
    Eigen::Map<Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> mapped_array(pts.data(), n_points, 3);

    pcl::PointCloud<pcl::PointXYZ>::Ptr orig_cloud(new pcl::PointCloud<pcl::PointXYZ>);
    pcl::io::loadPCDFile<pcl::PointXYZ>(pointcloud_filename, *orig_cloud);
    std::vector<int> indices;
    pcl::removeNaNFromPointCloud(*orig_cloud, *orig_cloud, indices);

    for (std::size_t i = 0; i < mapped_array.rows(); i++)
    {
      float orig_x = orig_cloud->at(i).x;
      float orig_y = orig_cloud->at(i).y;
      float orig_z = orig_cloud->at(i).z;

      ASSERT_FLOAT_EQ(mapped_array(i, 0), orig_x);
      ASSERT_FLOAT_EQ(mapped_array(i, 1), orig_y);
      ASSERT_FLOAT_EQ(mapped_array(i, 2), orig_z);
    }
  }

  TEST(ReadPCD, NanReadPCDTest)
  {
    std::string pointcloud_filename("nan_test.pcd");
    std::vector<float> pts;
    int n_points = read_pcd(pointcloud_filename, pts);

    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
    Eigen::Map<Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> mapped_array(pts.data(), n_points, 3);

    pcl::PointCloud<pcl::PointXYZ>::Ptr orig_cloud(new pcl::PointCloud<pcl::PointXYZ>);
    pcl::io::loadPCDFile<pcl::PointXYZ>(pointcloud_filename, *orig_cloud);
    std::vector<int> indices;
    pcl::removeNaNFromPointCloud(*orig_cloud, *orig_cloud, indices);

    for (std::size_t i = 0; i < mapped_array.rows(); i++)
    {
      float orig_x = orig_cloud->at(i).x;
      float orig_y = orig_cloud->at(i).y;
      float orig_z = orig_cloud->at(i).z;

      ASSERT_FLOAT_EQ(mapped_array(i, 0), orig_x);
      ASSERT_FLOAT_EQ(mapped_array(i, 1), orig_y);
      ASSERT_FLOAT_EQ(mapped_array(i, 2), orig_z);
    }
  }

}


#endif /* COMPARISON_UTILITY_UNIT_TEST */
