/**
* This file is part of ORB-SLAM3
*
* Copyright (C) 2017-2021 Carlos Campos, Richard Elvira, Juan J. Gómez Rodríguez, José M.M. Montiel and Juan D. Tardós, University of Zaragoza.
* Copyright (C) 2014-2016 Raúl Mur-Artal, José M.M. Montiel and Juan D. Tardós, University of Zaragoza.
*
* ORB-SLAM3 is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
* License as published by the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* ORB-SLAM3 is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
* the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License along with ORB-SLAM3.
* If not, see <http://www.gnu.org/licenses/>.
*/

#include <signal.h>
#include <stdlib.h>
#include <iostream>
#include <algorithm>
#include <fstream>
#include <chrono>
#include <ctime>
#include <sstream>

#include <condition_variable>

#include <opencv2/core/core.hpp>

#include <librealsense2/rs.hpp>
#include "librealsense2/rsutil.h"

#include <System.h>
#include <MapPoint.h>

using namespace std;
using namespace ORB_SLAM3;

bool b_continue_session;

void exit_loop_handler(int s)
{
    cout << "Finishing session" << endl;
    b_continue_session = false;
}

rs2_vector interpolateMeasure(const double target_time,
                              const rs2_vector current_data, const double current_time,
                              const rs2_vector prev_data, const double prev_time);

static rs2_option get_sensor_option(const rs2::sensor &sensor)
{
    // Sensors usually have several options to control their properties
    //  such as Exposure, Brightness etc.

    std::cout << "Sensor supports the following options:\n"
              << std::endl;

    // The following loop shows how to iterate over all available options
    // Starting from 0 until RS2_OPTION_COUNT (exclusive)
    for (int i = 0; i < static_cast<int>(RS2_OPTION_COUNT); i++)
    {
        rs2_option option_type = static_cast<rs2_option>(i);
        //SDK enum types can be streamed to get a string that represents them
        std::cout << "  " << i << ": " << option_type;

        // To control an option, use the following api:

        // First, verify that the sensor actually supports this option
        if (sensor.supports(option_type))
        {
            std::cout << std::endl;

            // Get a human readable description of the option
            const char *description = sensor.get_option_description(option_type);
            std::cout << "       Description   : " << description << std::endl;

            // Get the current value of the option
            float current_value = sensor.get_option(option_type);
            std::cout << "       Current Value : " << current_value << std::endl;

            //To change the value of an option, please follow the change_sensor_option() function
        }
        else
        {
            std::cout << " is not supported" << std::endl;
        }
    }

    uint32_t selected_sensor_option = 0;
    return static_cast<rs2_option>(selected_sensor_option);
}

bool is_number(const std::string& s)
{
    return !s.empty() && std::find_if(s.begin(), 
        s.end(), [](unsigned char c) { return !std::isdigit(c); }) == s.end();
}

int main(int argc, char **argv)
{
    if (argc < 3 || argc > 6)
    {
        cerr << endl
             << "Usage: ./executable path_to_vocabulary path_to_settings stop_number stop_mode file_name"
             << endl;
        return 1;
    }

    int stop_number = stoi(argv[argc - 3]);
    string stop_mode = string(argv[argc - 2]);
    string file_name = string(argv[argc - 1]);
    cout << stop_number << " " << stop_mode << " " << file_name << endl;

    struct sigaction sigIntHandler;

    sigIntHandler.sa_handler = exit_loop_handler;
    sigemptyset(&sigIntHandler.sa_mask);
    sigIntHandler.sa_flags = 0;

    sigaction(SIGINT, &sigIntHandler, NULL);
    b_continue_session = true;

    double offset = 0; // ms

    rs2::context ctx;
    rs2::device_list devices = ctx.query_devices();
    rs2::device selected_device;
    if (devices.size() == 0)
    {
        std::cerr << "No device connected, please connect a RealSense device" << std::endl;
        return 0;
    }
    else
        selected_device = devices[0];

    std::vector<rs2::sensor> sensors = selected_device.query_sensors();
    int index = 0;
    // We can now iterate the sensors and print their names
    for (rs2::sensor sensor : sensors)
        if (sensor.supports(RS2_CAMERA_INFO_NAME))
        {
            ++index;
            if (index == 1)
            {
                sensor.set_option(RS2_OPTION_ENABLE_AUTO_EXPOSURE, 1);
                sensor.set_option(RS2_OPTION_AUTO_EXPOSURE_LIMIT, 5000);
                sensor.set_option(RS2_OPTION_EMITTER_ENABLED, 0); // switch off emitter
            }
            // std::cout << "  " << index << " : " << sensor.get_info(RS2_CAMERA_INFO_NAME) << std::endl;
            get_sensor_option(sensor);
            if (index == 2)
            {
                // RGB camera (not used here...)
                sensor.set_option(RS2_OPTION_EXPOSURE, 100.f);
            }
        }

    // Declare RealSense pipeline, encapsulating the actual device and sensors
    rs2::pipeline pipe;
    // Create a configuration for configuring the pipeline with a non default profile
    rs2::config cfg;
    cfg.enable_stream(RS2_STREAM_INFRARED, 1, 640, 480, RS2_FORMAT_Y8, 30);

    // IMU callback
    std::mutex imu_mutex;
    std::condition_variable cond_image_rec;

    cv::Mat imCV;
    int width_img, height_img;
    double timestamp_image = -1.0;
    bool image_ready = false;
    int count_im_buffer = 0; // count dropped frames

    auto imu_callback = [&](const rs2::frame &frame)
    {
        std::unique_lock<std::mutex> lock(imu_mutex);

        if (rs2::frameset fs = frame.as<rs2::frameset>())
        {
            count_im_buffer++;

            double new_timestamp_image = fs.get_timestamp() * 1e-3;
            if (abs(timestamp_image - new_timestamp_image) < 0.001)
            {
                // cout << "Two frames with the same timeStamp!!!\n";
                count_im_buffer--;
                return;
            }

            rs2::video_frame ir_frameL = fs.get_infrared_frame(1);
            imCV = cv::Mat(cv::Size(width_img, height_img), CV_8U, (void *)(ir_frameL.get_data()), cv::Mat::AUTO_STEP);

            timestamp_image = fs.get_timestamp() * 1e-3;
            image_ready = true;

            lock.unlock();
            cond_image_rec.notify_all();
        }
    };

    rs2::pipeline_profile pipe_profile = pipe.start(cfg, imu_callback);

    rs2::stream_profile cam_left = pipe_profile.get_stream(RS2_STREAM_INFRARED, 1);

    rs2_intrinsics intrinsics_left = cam_left.as<rs2::video_stream_profile>().get_intrinsics();
    width_img = intrinsics_left.width;
    height_img = intrinsics_left.height;
    cout << "Left camera: \n";
    std::cout << " fx = " << intrinsics_left.fx << std::endl;
    std::cout << " fy = " << intrinsics_left.fy << std::endl;
    std::cout << " cx = " << intrinsics_left.ppx << std::endl;
    std::cout << " cy = " << intrinsics_left.ppy << std::endl;
    std::cout << " height = " << intrinsics_left.height << std::endl;
    std::cout << " width = " << intrinsics_left.width << std::endl;
    std::cout << " Coeff = " << intrinsics_left.coeffs[0] << ", " << intrinsics_left.coeffs[1] << ", " << intrinsics_left.coeffs[2] << ", " << intrinsics_left.coeffs[3] << ", " << intrinsics_left.coeffs[4] << ", " << std::endl;
    std::cout << " Model = " << intrinsics_left.model << std::endl;

    // Create SLAM system. It initializes all system threads and gets ready to process frames.
    string previous_File_Name;
    ORB_SLAM3::System SLAM(argv[1], argv[2], ORB_SLAM3::System::MONOCULAR, true, 0, previous_File_Name);
    auto atlas = SLAM.mpAtlas;
    float imageScale = SLAM.GetImageScale();

    double timestamp;
    cv::Mat im;

    double t_resize = 0.f;
    double t_track = 0.f;

    std::vector<MapPoint *> map;
    auto start = chrono::steady_clock::now();
    std::chrono::steady_clock::time_point end;
    bool stop = false;
    int i = 0;
    while (!stop)
    {
        std::vector<rs2_vector> vGyro;
        std::vector<double> vGyro_times;
        std::vector<rs2_vector> vAccel;
        std::vector<double> vAccel_times;

        {
            std::unique_lock<std::mutex> lk(imu_mutex);
            if (!image_ready)
                cond_image_rec.wait(lk);

            if (count_im_buffer > 1)
                cout << count_im_buffer - 1 << " dropped frs\n";
            count_im_buffer = 0;

            timestamp = timestamp_image;
            im = imCV.clone();

            image_ready = false;
        }

        if (imageScale != 1.f)
        {
            int width = im.cols * imageScale;
            int height = im.rows * imageScale;
            cv::resize(im, im, cv::Size(width, height));
        }
        // Stereo images are already rectified.
        SLAM.TrackMonocular(im, timestamp);
        if (i == 399)
            map = atlas->GetAllMapPoints();
        if (stop_mode == "0")
        {
            auto end = chrono::steady_clock::now();
            auto delay = chrono::duration_cast<chrono::seconds>(end - start).count();
            cout << "Delay " << delay << endl;
            stop = (delay > stop_number);
        }
        else if (stop_mode == "1")
        {
            i ++;
            cout << "Image " << i << endl;
            stop = (i > stop_number);
        }
    }
    std::ofstream mapFile;
    mapFile.open("/app/datasets/maps/" + file_name + ".csv");
    mapFile << "x y z" << endl;
    std::string sep = " ";
    for (auto point : map)
    {
        auto pos = point->GetWorldPos();
        mapFile << pos(0) << sep << pos(1) << sep << pos(2) << endl;
        cout << "x=" << pos(0) << ", y=" << pos(1) << ", z=" << pos(2) << endl;
    }
    mapFile.close();

    SLAM.Shutdown();
    cout << "System shutdown!\n";
    return EXIT_SUCCESS;
}