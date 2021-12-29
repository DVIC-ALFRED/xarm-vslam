REALSENSE_READY_IM_NAME=lmwafer/realsense-ready
REALSENSE_READY_IM_TAG=2.0-ubuntu18.04
REALSENSE_READY_CONT_NAME=realsense-container

ORB_SLAM_DIRECTORY=orb-slam-3/
ORB_SLAM_IM_NAME=lmwafer/orb-slam-3-ready
ORB_SLAM_IM_TAG=1.0-ubuntu18.04
ORB_SLAM_CONT_NAME=orb-container # You will need to apply the exact same name to container_name in orb-slam/docker-compose.yml

default: up-orb enter-orb

up-orb:
	sudo xhost +local:root && cd ${ORB_SLAM_DIRECTORY} && sudo docker-compose up -d

enter-orb:
	clear && docker exec -it ${ORB_SLAM_CONT_NAME} bash

down-orb:
	cd ${ORB_SLAM_DIRECTORY} && docker-compose down

build-orb:
	cd ${ORB_SLAM_DIRECTORY} && sudo docker build -t ${ORB_SLAM_IM_NAME}:${ORB_SLAM_IM_TAG} .


up-realsense:
	sudo xhost +local:root && cd realsense-ready-v2/ && sudo docker-compose up -d

enter-realsense:
	clear && docker exec -it ${REALSENSE_READY_CONT_NAME} bash

down-realsense:
	cd realsense-ready-v2/ && docker-compose down

build-realsense:
	cd realsense-ready-v2/ && sudo docker build -t ${REALSENSE_READY_IM_NAME}:${REALSENSE_READY_IM_TAG} .

emergency: down-orb up-orb
	docker exec -it ${ORB_SLAM_CONT_NAME} rs-multicam