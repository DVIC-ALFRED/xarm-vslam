# xarm-vslam

## (SLAM) 'orb-slam2' image usage

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

## 'realsense-ready' image usage

Build images:  
```bash
make build-realsense-ready
# or
make build-orb-slam
``
