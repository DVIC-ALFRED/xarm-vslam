REALSENSE_READY_IM_NAME=lmwafer/realsense-ready
REALSENSE_READY_IM_TAG=2.0-ubuntu18.04
REALSENSE_READY_CONT_NAME=realsense-container

ORB_SLAM_2_DIRECTORY=orb-slam-2/
ORB_SLAM_2_IM_NAME=lmwafer/orb-slam-2-ready
ORB_SLAM_2_IM_TAG=1.0-ubuntu18.04
ORB_SLAM_2_CONT_NAME=orb-2-container # You will need to apply the exact same name to container_name in orb-slam/docker-compose.yml

ORB_SLAM_3_DIRECTORY=orb-slam-3/
ORB_SLAM_3_IM_NAME=lmwafer/orb-slam-3-ready
ORB_SLAM_3_IM_TAG=1.1b-ubuntu18.04
ORB_SLAM_3_CONT_NAME=orb-3-container # You will need to apply the exact same name to container_name in orb-slam/docker-compose.yml

default: up-orb-3 enter-orb-3


up-orb-2:
	sudo xhost +local:root && cd ${ORB_SLAM_2_DIRECTORY} && sudo docker-compose up -d

enter-orb-2:
	clear && docker exec -it ${ORB_SLAM_2_CONT_NAME} bash

down-orb-2:
	cd ${ORB_SLAM_2_DIRECTORY} && docker-compose down

build-orb-2:
	cd ${ORB_SLAM_2_DIRECTORY} && sudo docker build -t ${ORB_SLAM_2_IM_NAME}:${ORB_SLAM_2_IM_TAG} .

demo-orb-2: down-orb-2 up-orb-2
	docker exec -it -w /app ${ORB_SLAM_2_CONT_NAME} make demo


up-orb-3:
	sudo xhost +local:root && cd ${ORB_SLAM_3_DIRECTORY} && sudo docker-compose up -d

enter-orb-3:
	clear && docker exec -it ${ORB_SLAM_3_CONT_NAME} bash

down-orb-3:
	cd ${ORB_SLAM_3_DIRECTORY} && docker-compose down

build-orb-3:
	cd ${ORB_SLAM_3_DIRECTORY} && sudo docker build -t ${ORB_SLAM_3_IM_NAME}:${ORB_SLAM_3_IM_TAG} .

demo-orb-3-dts: down-orb-3 up-orb-3
	docker exec -it -w /app ${ORB_SLAM_3_CONT_NAME} make demo-datasets

prepare-orb-3-dts:
	docker exec -it -w /app ${ORB_SLAM_3_CONT_NAME} make prepare

demo-orb-3-rt: down-orb-3 up-orb-3
	docker exec -it -w /app ${ORB_SLAM_3_CONT_NAME} make demo-realtime


up-realsense:
	sudo xhost +local:root && cd realsense-ready-v2/ && sudo docker-compose up -d

enter-realsense:
	clear && docker exec -it ${REALSENSE_READY_CONT_NAME} bash

down-realsense:
	cd realsense-ready-v2/ && docker-compose down

build-realsense:
	cd realsense-ready-v2/ && sudo docker build -t ${REALSENSE_READY_IM_NAME}:${REALSENSE_READY_IM_TAG} .
	
demo-realsense: down-realsense up-realsense
	docker exec -it ${REALSENSE_READY_CONT_NAME} rs-multicam