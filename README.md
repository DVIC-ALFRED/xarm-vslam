# Introduction

Every image preceded with ***(VSLAM)*** is an image made for a specific algorithm. 

# Images

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
# or
make build-orb-slam
```
# "Demo in 5 minutes" like emergency
