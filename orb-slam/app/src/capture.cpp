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
    // Declare depth colorizer for pretty visualization of depth data
    rs2::colorizer color_map;

    // Declare RealSense pipeline, encapsulating the actual device and sensors
    rs2::pipeline pipe;
    // Start streaming with default recommended configuration
    pipe.start();

    // Capture 30 frames to give autoexposure, etc. a chance to settle
    for (auto i = 0; i < 30; ++i)
        pipe.wait_for_frames();

    // Wait for the next set of frames from the camera. Now that autoexposure, etc.
    // has settled, we will write these to disk
    std::stringstream filename;
    filename << "dataset/rbg.txt";
    std::ofstream txtfile;
    txtfile.open(filename.str());
    txtfile << "# color images"
            << "\n";
    for (size_t i = 0; i < 20; ++i)
    {
        for (auto &&frameset : pipe.wait_for_frames())
        {
            // We can only save video frames as pngs, so we skip the rest
            if (auto vf = frameset.as<rs2::video_frame>())
            {
                auto stream = frameset.get_profile().stream_type();
                // Use the colorizer to get an rgb image for the depth stream
                if (vf.is<rs2::depth_frame>())
                    vf = color_map.process(frameset);

                if (vf.get_profile().stream_name() == "Color")
                {
                    std::stringstream png_file;
                    // -> Save the image in the following format : "<frame_number>.png"
                    png_file << "dataset/rgb/" << vf.get_frame_number() << ".png";
                    stbi_write_png(png_file.str().c_str(), vf.get_width(), vf.get_height(),
                                   vf.get_bytes_per_pixel(), vf.get_data(), vf.get_stride_in_bytes());

                    // -> Save the timestamp in the following format : "<time_stamp> rgb/<frame_number>.png"
                    txtfile << std::fixed << vf.get_timestamp() << " rgb/" << vf.get_frame_number() << ".png"
                            << "\n";

                    // -> Let the user know which images are being saved
                    std::cout << std::fixed << vf.get_timestamp() << " rgb/" << vf.get_frame_number() << ".png" << std::endl;
                }
            }
        }
    }
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