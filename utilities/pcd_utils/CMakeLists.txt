cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
set (CMAKE_CXX_STANDARD 14)
project(read_cloud_tester)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/609281088cfefc76f9d0ce82e1ff6c30cc3591e5.zip
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

find_package(PCL 1.2 REQUIRED)

include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

enable_testing()

add_executable(
    unit_test
    unit_test.cpp
)
target_link_libraries(
  unit_test
  gtest_main
  ${PCL_LIBRARIES}
)

include(GoogleTest)
gtest_discover_tests(unit_test)
