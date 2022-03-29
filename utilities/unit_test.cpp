#ifndef COMPARISON_UTILITY_UNIT_TEST
#define COMPARISON_UTILITY_UNIT_TEST

#include <string>
#include <Eigen/Core>
#include <Eigen/Geometry>
#include <pcl/io/pcd_io.h>
#include <pcl/filters/filter.h>
#include <pcl/common/transforms.h>
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

    TEST(ApplyAffine, ApplyAffineTest)
  {
    std::string pointcloud_filename("test.pcd");
    std::vector<float> pts;
    int n_points = read_pcd(pointcloud_filename, pts);
    Eigen::Vector3f vect(1,1,1);
    Eigen::Transform<float,3,Eigen::Affine> trans = Eigen::Translation3f(vect) * Eigen::AngleAxisf(30,vect);
    Eigen::Matrix4f affine_trans = trans.matrix();
    apply_affine(pts, n_points, affine_trans);
    
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
    pcl::io::loadPCDFile<pcl::PointXYZ> ("test.pcd", *cloud);
    std::vector<int> indices;
    pcl::removeNaNFromPointCloud(*cloud, *cloud, indices);
    pcl::transformPointCloud(*cloud, *cloud, affine_trans);

    Eigen::Map<Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> mapped_array(pts.data(), n_points, 3);
    for (std::size_t i = 0; i < mapped_array.rows(); i++)
    {
      float orig_x = cloud->at(i).x;
      float orig_y = cloud->at(i).y;
      float orig_z = cloud->at(i).z;

      ASSERT_FLOAT_EQ(mapped_array(i, 0), orig_x);
      ASSERT_FLOAT_EQ(mapped_array(i, 1), orig_y);
      ASSERT_FLOAT_EQ(mapped_array(i, 2), orig_z);
    }

    ASSERT_EQ(pts.size()/3, cloud->size());
  }

}


#endif /* COMPARISON_UTILITY_UNIT_TEST */
