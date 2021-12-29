# Introduction

## Repository

This is the repository of the Visual Simultaneous Localization and Mapping algorithms running within ALFRED. As there are multiple vLSAMs (not working at the same time) each one lays in its own Docker image. 

## Images

Every image preceded with ***(vSLAM Algorithm)*** is made for a specific VSLAM algorithm and does not depend on any other ***(vSLAM Algorithm)*** image. 

# (vSLAM Algorithm) '**ORB-SLAM 2**'
This images contains a pre-installed ORB-SLAM 2 in **/dpds/ORB_SLAM2**. See on Docker Hub [lmwafer/orb-slam2-ready](https://hub.docker.com/r/lmwafer/orb-slam2-ready). 

It is based on Docker image realsense-ready to use Intel RealSense 2 SDK and cameras. See on Docker Hub [lmwafer/realsense-ready](https://hub.docker.com/r/lmwafer/realsense-ready)

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
  to get the id of your GPU. See [Enabling GPU access with Compose](https://docs.docker.com/compose/gpu-support/)

## Image installation

The tag may be outdated. See on [Dockerhub](https://hub.docker.com/r/lmwafer/orb-slam2-ready/tags).

```bash
docker pull lmwafer/orb-slam2-ready:1.0-ubuntu18.04
```
  
## Image dataset demo

Without a camera you can still run the provided demo on known datasets. We will use TUM. 

### Setup demo
1. Run this in **xarm-vlsam** directory to create and enter a container
    ```bash
    make up-orb-2 enter-orb-2
    ```
2. Then type this inside the container to download and extract 4 TUM datasets
    ```bash
    cd /app && make prepare
    ```

## Image usage
All the commands need to be run in **xarm-vlsam** directory. 

Run a container (uses **orb-slam-3/docker-compose.yml**)
```bash
make up-orb-2
```

Enter the upped container
```bash
make enter-orb-2
```

Shut down ORB SLAM container (will remove the container, only data in **/app** will be saved)
```bash
make down-orb-2
```

Build orb-slam image (uses **orb-slam-3/Dockerfile**)
```bash
make build-orb-2
```

# (vSLAM Algorithm) '**ORB-SLAM 3**'
Almost like ORB-SLAM 2, this images contains a pre-installed ORB-SLAM 3 in **/dpds/ORB_SLAM3**. See on Docker Hub [lmwafer/orb-slam-3-ready](https://hub.docker.com/r/lmwafer/orb-slam-3-ready). 

It is based on Docker image realsense-ready to use Intel RealSense 2 SDK and cameras. See on Docker Hub [lmwafer/realsense-ready](https://hub.docker.com/r/lmwafer/realsense-ready/tags)

## Image prerequisites

- Docker (tested with Docker 20.10.7), see [Install Docker Engine](https://docs.docker.com/engine/install/)

- Docker Compose (tested with Docker Compose 1.29.2), see [Install Docker Compose](https://docs.docker.com/compose/install/)
  You may have a `/usr/local/bin/docker-compose: no such file or directory` error. In this case, use
  ```bash
  sudo mkdir /usr/local/bin/docker-compose
  ```
  before restarting the installation process

- Nvidia Container Toolkit (tested with ubuntu20.04 distribution), see [NVIDIA Container Toolkit Installation Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

- The `device id` parameter in **orb-slam/docker-compose.yml** may take another number on different machines. Use
  ```bash
  lshw -c display
  ```
  to get the id of your GPU. See [Enabling GPU access with Compose](https://docs.docker.com/compose/gpu-support/)

## Image installation

The tag may be outdated. See on [Dockerhub](https://hub.docker.com/r/lmwafer/orb-slam-3-ready/tags).

```bash
docker pull lmwafer/orb-slam-3-ready:1.0-ubuntu18.04
```
  
## Image real-time demo

With a realsense camera aviable you may want a cool real-time demo of the vSLAM. 
1. Connect an Intel Realsense D435i or D435 via USB
2. Run this in **xarm-vlsam** directory to create and enter a container
    ```bash
    make demo-orb-3-rt
    ```

## Image dataset demo

Without a camera you can still run the provided demo on known datasets. We will use TUM. 

All the commands need to be run in **xarm-vlsam** directory. 
### Setup demo
```bash
make prepare-orb-3-dts
```

### Run demo

```bash
make demo-orb-3-dts
```

## Image usage
All the commands need to be run in **xarm-vlsam** directory. 

Get inside a freshly new container (basically `up` + `enter`)
```bash
make
```

Start an *orb-3-container* (uses **orb-slam-3/docker-compose.yml**)
```bash
make up-orb-3
```

Enter running *orb-3-container*
```bash
make enter-orb-3
```

Stop running *orb-3-container* (and removes it, only data in **/app** will be saved)
```bash
make down-orb-3
```

Build *orb-slam-3-ready* image (uses **orb-slam-3/Dockerfile**)
```bash
make build-orb-3
```

# (Camera SDK) '**realsense-ready**'

See on Docker Hub [lmwafer/realsense-ready](https://hub.docker.com/r/lmwafer/realsense-ready). 

## Image prerequisites

Nothing except an Internet connexion !

## Image installation

The tag may be outdated. See on [Dockerhub](https://hub.docker.com/r/lmwafer/realsense-ready/tags).

```bash
docker pull lmwafer/realsense-ready:ubuntu18.04
```

## Image demo

This demo displays a *depth* vs *camera* video stream.

1. Connect an Intel Realsense camera via USB.
2. Run this in **xarm-vlsam** directory
    ```bash
    make demo-realsense # /!\ Remove running orb-slam containers, it's an emergency huh
    ```
3. Make this shitty window appear to people like an insane feature.

## Image usage

A core image with Intel Realsense SDK pre-installed and all common problems already fixed <3 ! You need to run the command in **xarm-vslam** directory. 

Start a container (uses **realsense-ready-v2/docker-compose.yml**)
```bash
make up-realsense
```

Enter running *realsense-container*
```bash
make enter-realsense
```

Stop running *realsense-container* (and removes it, only data in **/app** will be saved)
```bash
make down-realsense
```

Build realsense-ready image (uses **realsense-ready-v2/Dockerfile**)
```bash
make build-realsense
```