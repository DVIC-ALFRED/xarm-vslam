#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API

#include <fstream>  // File IO
#include <iostream> // Terminal IO
#include <sstream>  // Stringstreams

// 3rd party header for writing png files
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

// This sample captures 30 frames and writes the last frame to disk.
// It can be useful for debugging an embedded system with no display.
int main(int argc, char *argv[])
try
{
    // window app(1280, 720, "LMsCapture");
    // Declare depth colorizer for pretty visualization of depth data
    rs2::colorizer color_map;

    // Declare RealSense pipeline, encapsulating the actual device and sensors
    auto pipe = std::make_shared<rs2::pipeline>();

    // Declare config object to only enable color stream => remove IR stream dots
    rs2::config cfg1;
    cfg1.enable_stream(RS2_STREAM_COLOR, -1, 640, 360, rs2_format::RS2_FORMAT_ANY, 0);
    cfg1.enable_record_to_file("a.bag");

    // Start streaming with default recommended configuration
    pipe->start(cfg1);

    // Capture 30 frames to give autoexposure, etc. a chance to settle
    for (auto i = 0; i < 30; ++i)
        pipe->wait_for_frames();

    // Wait for the next set of frames from the camera. Now that autoexposure, etc.
    // has settled, we will write these to disk
    std::cout << "Début capture" << std::endl;

    std::vector<rs2::frame> frames;
    for (size_t i = 0; i < 30; ++i)
    {
        rs2::frameset data = pipe->wait_for_frames();
    }
    std::cout << pipe->get_active_profile().get_device().as<rs2::playback>() << std::endl;
    pipe->stop();
    pipe = std::make_shared<rs2::pipeline>();

    std::cout << "Fin capture, début restitution" << std::endl;

    std::stringstream png_file;

    // Declare txt stream to save timestamps
    std::stringstream filename;
    filename << "dataset/rbg.txt";
    std::ofstream txtfile;
    txtfile.open(filename.str());
    txtfile << "# color images"
            << "\n";

    // pipe = std::make_shared<rs2::pipeline>();
    rs2::config cfg2;
    cfg2.enable_device_from_file("a.bag");
    pipe->start(cfg2);
    std::cout << pipe->get_active_profile().get_device().as<rs2::playback>() << std::endl;
    for (int i = 0; i < 30; i++)
    {
        for (auto &&frameset : pipe->wait_for_frames())
        {
            if (rs2::video_frame vf = frameset.as<rs2::video_frame>())
            {
                if (vf.get_profile().stream_name() == "Color")
                {
                    // -> Save the image in the following format : "<frame_number>.png"
                    png_file << "images/" << vf.get_frame_number() << ".png";
                    stbi_write_png(png_file.str().c_str(), vf.get_width(), vf.get_height(),
                                   vf.get_bytes_per_pixel(), vf.get_data(), vf.get_stride_in_bytes());

                    // -> Save the timestamp in the following format : "<time_stamp> rgb/<frame_number>.png"
                    txtfile << std::fixed << vf.get_timestamp() << " rgb/" << vf.get_frame_number() << ".png"
                            << "\n";

                    // -> Let the user know which images are being saved
                    std::cout << std::fixed << vf.get_timestamp() << " images/" << vf.get_frame_number() << ".png" << std::endl;
                }
            }
        }
    }
    pipe->stop();
    txtfile.close();

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