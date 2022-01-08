cmake_minimum_required(VERSION 3.10.2)
project(Demarrage)

IF(NOT CMAKE_BUILD_TYPE)
  SET(CMAKE_BUILD_TYPE Release)
ENDIF()

MESSAGE("Build type: " ${CMAKE_BUILD_TYPE})

#-> Strange flags stuff from ORB
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O3")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -march=native")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -march=native")

#-? Check C++11 or C++0x support
include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)
if(COMPILER_SUPPORTS_CXX11)
   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
   add_definitions(-DCOMPILEDWITHC11)
   message(STATUS "Using flag -std=c++11.")
elseif(COMPILER_SUPPORTS_CXX0X)
   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
   add_definitions(-DCOMPILEDWITHC0X)
   message(STATUS "Using flag -std=c++0x.")
else()
   message(FATAL_ERROR "The compiler ${CMAKE_CXX_COMPILER} has no C++11 support. Please use a different C++ compiler.")
endif()

#-> Look for dependencies
#-? This will fill <package>_INCLUDE_DIR and <package>_LIBRARY
find_package(OpenCV 4.5)
find_package(Eigen3 3.1.0 REQUIRED)
find_package(Pangolin REQUIRED)
find_package(realsense2)

#-? Since find_package(ORB-SLAM3 REQUIRED) does not work (ORB is not a library) include its .so
set(ORB_DIR /dpds/ORB_SLAM3)
set(ORB_LIBS /dpds/ORB_SLAM3/lib/libORB_SLAM3.so)
set(ORB_INCLUDE_DIR /dpds/ORB_SLAM3/include)

set(DBOW2_LIBS /dpds/ORB_SLAM3/Thirdparty/DBoW2/lib/libDBoW2.so)
set(DBOW2_INCLUDE_DIR /dpds/ORB_SLAM3/Thirdparty/DBoW2/DBoW2)

add_executable(${PROJECT_NAME} src/main.cpp)

# If RealSense SDK is found the library is added and its examples compiled
if(realsense2_FOUND)
    include_directories(${PROJECT_NAME}
    ${realsense_INCLUDE_DIR}
    )
    target_link_libraries(${PROJECT_NAME}
    ${realsense2_LIBRARY}
    )
endif()

include_directories(${PROJECT_SOURCE_DIR} 
${ORB_INCLUDE_DIR}
${DBOW2_INCLUDE_DIR}
${ORB_DIR}
${ORB_INCLUDE_DIR}/CameraModels
${ORB_DIR}/Thirdparty/Sophus
${EIGEN3_INCLUDE_DIR}
${Pangolin_INCLUDE_DIRS}
)

#-> Looks for .so files
#-? .so are shared object, no matter their position : they contains all the library features needed
#-? Function signatures are located in the lib include directory
target_link_libraries(${PROJECT_NAME} 
${ORB_LIBS} 
${OpenCV_LIBS} 
${DBOW2_LIBS}
${ORB_DIR}/Thirdparty/g2o/lib/libg2o.so
${EIGEN3_LIBS}
${Pangolin_LIBRARIES}
-lboost_serialization
-lcrypto
)