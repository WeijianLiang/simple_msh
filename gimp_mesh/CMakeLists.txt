cmake_minimum_required(VERSION 3.12)
project(gimp_mesh)

set(CMAKE_CXX_STANDARD 11)

# Eigen
find_package(Eigen3 REQUIRED)
include_directories(${EIGEN3_INCLUDE_DIR})

add_executable(gimp_mesh main.cpp)
