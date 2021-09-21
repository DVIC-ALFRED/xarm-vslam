REALSENSE_READY_IM_NAME=lmwafer/realsense-ready
REALSENSE_READY_IM_TAG=ubuntu18.04
ORB_SLAM_IM_NAME=
ORB_SLAM_IM_TAG=

all: up-orb

up-orb:
	cd orb-slam && docker-compose up -d

down-orb:
	cd orb-slam && docker-compose down

build-realsense-ready:
	cd realsense-ready && docker build -t ${REALSENSE_READY_IM_NAME}:${REALSENSE_READY_IM_TAG} .

build-orb-slam:
	cd realsense-ready && docker build -t ${ORB_SLAM_IM_NAME}:${ORB_SLAM_IM_TAG} .
