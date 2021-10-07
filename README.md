# Introduction

## Repository

This is the repository of the Visual Simultaneous Localization and Mapping algorithms running within ALFRED. As there will probably be multiple VLSAMs (not working at the same time) each one lays in its own Docker image. 

## Images

Every image preceded with ***(VSLAM)*** is made for a specific VSLAM algorithm and does not depend on any other ***(VSLAM)*** image. 


# (VSLAM) '**orb-slam2**'

See on Docker Hub [lmwafer/orb-slam2-ready](https://hub.docker.com/r/lmwafer/orb-slam2-ready). 

## Image prerequisites

- Docker (tested with Docker 20.10.7), see [Install Docker Engine](https://docs.docker.com/engine/install/)

- Docker Compose (tested with Docker Compose 1.29.2), see [Install Docker Compose](https://docs.docker.com/compose/install/)  
  You may have a `/usr/local/bin/docker-compose: no such file or directory` error. In this case, use
  ```bash
  sudo mkdir /usr/local/bin/docker-compose
  ```
  before restarting the installation process.

- Nvidia Container Toolkit (tested with ubuntu20.04 distribution), see [NVIDIA Container Toolkit Installation Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

- The `device id` parameter in **orb-slam/docker-compose.yml** may take another number on different machines. Use
  ```bash
  lshw -c display
  ```
  to get the id of your GPU. 
  
## <a name="install"> Image demo </a>

You may want a cool demo of ORM-SLAM2. For such applications ORB provides already compatible examples that come alongside with common datasets. We will use TUM. 

1. First, go to the directory where you will place the dataset. 
```bash
cd /app/lib
```
2. Download the dataset from its website.
```bash
wget https://vision.in.tum.de/rgbd/dataset/freiburg1/rgbd_dataset_freiburg1_xyz.tgz
```
3. Untar the dataset.
```bash
tar -xzf rgbd_dataset_freiburg1_xyz.tgz
```
4. You can now remove the downloaded file to keep only the directory !
```bash
rm rgbd_dataset_freiburg1_xyz.tgz
```
Everytime you need to use it, type as last command argument the directory name. Here **rgbd_dataset_freiburg1_xyz**. See [TUM Dataset demo](#demo).

## Image usage

The image is based on a ***realsense-ready*** image.
All the commands need to be run in **xarm-vlsam** directory. 

Get inside a freshly new container (basically `up` + `enter`)
```bash
make
```

Run a container (uses **orb-slam/docker-compose.yml**)
```bash
make up-orb
```

Enter the upped container
```bash
make enter-orb
```

Shut down ORB SLAM container (will remove the container)
```bash
make down-orb
```

Build orb-slam image (uses **orb-slam/Dockerfile**)
```bash
make build-orb-slam
```


# '**realsense-ready**'

See on Docker Hub [lmwafer/realsense-ready](https://hub.docker.com/r/lmwafer/realsense-ready). 

## Image prerequisites

Nothing except an Internet connexion !

## Image usage

A core image with Intel Realsense SDK pre-installed and all common problems already fixed <3 ! You need to run the command in **xarm-vslam** directory. 

Build images (uses **realsense-ready/Dockerfile**)
```bash
make build-realsense-ready
```

# "Demo in 5 minutes" like emergency

## For a noice realtime *depth* vs *camera* display

1. Make sure an Intel Realsense camera is connected via USB.
2. Run this in **xarm-vlsam** directory
```bash
make emergency # /!\ Rm running orb-slam containers, it's an emergency huh
```
3. Enter sudo password if necessary.
4. Make this shitty window appear to people like an insane feature.

## <a name="demo"> For an insane non-realtime VSLAM demo </a>

**You need to have a dataset installed in /app/lib, see [TUM dataset installation](#install)**. 

1. Run this in **xarm-vlsam** directory
```bash
make # /!\ Rm running orb-slam containers, it's an emergency huh
``` 
2. In the container, enter this
```bash
cd /dpds/ORB_SLAM2/ && \
./Examples/Monocular/mono_tum \
Vocabulary/ORBvoc.txt \
Examples/Monocular/TUM1.yaml \
/app/lib/rgbd_dataset_freiburg1_xyz 
```
3. Enter sudo password if necessary. 