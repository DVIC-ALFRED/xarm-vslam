# Introduction

This is the repository of the Visual Simultaneous Localization and Mapping algorithms running within ALFRED. As there will probably be multiple VLSAMs (not working at the same time) each one lays in its own Docker image. 

# Images

Every image preceded with ***(VSLAM)*** is made for a specific VSLAM algorithm and does not depend on any other ***(VSLAM)*** image. 

## (VSLAM) 'orb-slam2' docker image usage

The image is based on a realsense-ready image. 

Run ORB SLAM container:  
```bash
make up-orb
# and to access container:
docker exec -it realsense-ready bash
```

Shut down ORB SLAM container:  
```bash
make down-orb
```

Build orb-slam image:  
```bash
make build-orb-slam
```

## 'realsense-ready' docker image usage

A core image with Intel Realsense SDK pre-installed and all common problems already fixed ! <3

Build images:  
```bash
make build-realsense-ready
```

# "Demo in 5 minutes" like emergency
