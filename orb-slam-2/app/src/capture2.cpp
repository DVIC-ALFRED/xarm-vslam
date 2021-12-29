#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API
#include <fstream>  // File IO
#include <iostream> // Terminal IO
#include <sstream>  // Stringstreams
#include <opencv2/opencv.hpp>

// 3rd party header for writing png files
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

cv::Mat frame_to_mat(const rs2::frame& f);

// This sample captures 30 frames and writes the last frame to disk.
// It can be useful for debugging an embedded system with no display.
int main(int argc, char *argv[])
try
{
    // Declare depth colorizer for pretty visualization of depth data
    rs2::colorizer color_map;

    rs2::config cfg;
    cfg.enable_stream(RS2_STREAM_COLOR, -1, 640, 360, rs2_format::RS2_FORMAT_ANY, 0);
    // cfg.enable_stream(RS2_STREAM_DEPTH, -1, 640, 360, rs2_format::RS2_FORMAT_ANY, 0);
    
    // Declare RealSense pipeline, encapsulating the actual device and sensors
    rs2::pipeline pipe;
    // Start streaming with default recommended configuration
    pipe.start(cfg);
    cv::Size rgbSize, depthSize;

    const auto depthWindowName = "Depth";
    const auto rgbWindowName = "RGB";
    cv::namedWindow(depthWindowName, cv::WINDOW_AUTOSIZE);
    cv::namedWindow(rgbWindowName, cv::WINDOW_AUTOSIZE);
    
    while (cv::waitKey(1) < 0 && cvGetWindowHandle(depthWindowName) && cvGetWindowHandle(rgbWindowName))
    {
        //get frames and align
        rs2::frameset data = pipe.wait_for_frames();
        rs2::frame depth = data.get_depth_frame();
        rs2::frame rgb = data.get_color_frame();
        if (!depth)
            continue;
        
        //get opencv matrices
        // cv::Mat depthMat = frame_to_mat(color_map(depth));
        cv::Mat rgbMat = frame_to_mat(rgb);
        
        // show images
        // imshow(depthWindowName, depthMat);
        imshow(rgbWindowName, rgbMat);
    }

    return EXIT_SUCCESS;
}
catch (const rs2::error &e)
{
    std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n    " << e.what() << std::endl;
    return EXIT_FAILURE;
}
catch (const std::exception &e)
{
    std::cerr << e.what() << std::endl;
    return EXIT_FAILURE;
}

cv::Mat frame_to_mat(const rs2::frame& f)
{
    using namespace cv;
    using namespace rs2;

    auto vf = f.as<video_frame>();
    const int w = vf.get_width();
    const int h = vf.get_height();

    if (f.get_profile().format() == RS2_FORMAT_BGR8)
    {
        return Mat(Size(w, h), CV_8UC3, (void*)f.get_data(), Mat::AUTO_STEP);
    }
    else if (f.get_profile().format() == RS2_FORMAT_RGB8)
    {
        auto r = Mat(Size(w, h), CV_8UC3, (void*)f.get_data(), Mat::AUTO_STEP);
        cvtColor(r, r, CV_RGB2BGR);
        return r;
    }
    else if (f.get_profile().format() == RS2_FORMAT_Z16)
    {
        return Mat(Size(w, h), CV_16UC1, (void*)f.get_data(), Mat::AUTO_STEP);
    }
    else if (f.get_profile().format() == RS2_FORMAT_Y8)
    {
        return Mat(Size(w, h), CV_8UC1, (void*)f.get_data(), Mat::AUTO_STEP);
    }

    throw std::runtime_error("Frame format is not supported yet!");
}