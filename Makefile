REALSENSE_READY_IM_NAME=lmwafer/realsense-ready
REALSENSE_READY_IM_TAG=ubuntu18.04
ORB_SLAM_IM_NAME=orb-ready
ORB_SLAM_IM_TAG=latest
ORB_SLAM_CONT_NAME=orb-container # You will need to apply the exact same name to container_name in orb-slam/docker-compose.yml

all: up-orb enter-orb

up-orb:
	sudo xhost +local:root && cd orb-slam && sudo docker-compose up -d

enter-orb:
	clear && docker exec -it ${ORB_SLAM_CONT_NAME} bash

down-orb:
	cd orb-slam && docker-compose down

build-orb-slam:
	cd orb-slam && sudo docker build -t ${ORB_SLAM_IM_NAME}:${ORB_SLAM_IM_TAG} .

build-realsense-ready:
	cd realsense-ready && sudo docker build -t ${REALSENSE_READY_IM_NAME}:${REALSENSE_READY_IM_TAG} .

emergency: down-orb up-orb
	docker exec -it ${ORB_SLAM_CONT_NAME} rs-multicam