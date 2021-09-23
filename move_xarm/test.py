import signal
import threading
import time
from queue import Queue
import sys

import numpy as np

import xarm_hand_control as xhc
from xarm.wrapper import XArmAPI


VIDEO_INDEX=4
ARM_IP = "172.21.72.200"

speed=40
mvacc=10000

arm: XArmAPI = None

COMMAND_QUEUE = Queue()

def sigint_handler(sig, frame):
    print("\nSIGINT Captured, terminating")
    if arm is not None:
        arm.set_state(4)
        arm.disconnect()

    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)


def robot_start() -> XArmAPI:
    arm = "ALFRED"

    connected = False
    while not connected:
        try:
            arm = XArmAPI(ARM_IP, do_not_open=True)
            arm.connect()
            connected = True
        except:
            print("arm is not online. trying again in 3 seconds...")
            time.sleep(3)

    arm.set_world_offset([0, 0, 0, 0, 0, 0])
    time.sleep(1)

    arm.clean_error()
    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)

    init_pos=[206.9, 0, 258.7, 180, 0,0]
    ret = arm.set_position(*init_pos,
        radius=-1, is_radian=False, wait=True, speed=speed, mvacc=mvacc, relative=False)

    time.sleep(1)
    print("arm started")

    return arm

def worker(arm: XArmAPI):
    radius=-1
    #arm.set_servo_angle(1,100,speed,mvacc,wait=False,radius=radius)
    pos=arm.position
    pos=[round(num, 1) for num in pos]
    x,y=pos[0],pos[1]
    length=np.sqrt(x**2+y**2)
    angle=100*np.pi/180
    x,y=length*np.cos(angle),length*np.sin(angle)
    new_pos=[x,y]+pos[2::]
    arm.set_position(*new_pos,radius=radius, wait=True, speed=speed,mvacc=mvacc,relative=False)
    new_pos[2]+=100
    arm.set_position(*new_pos,radius=radius, wait=True, speed=speed,mvacc=mvacc,relative=False)

def worker2(arm: XArmAPI):
    arm.set_servo_angle(1,90,speed=speed,mvacc=mvacc,wait=True)
    pos=arm.position
    pos=[round(num, 1) for num in pos]
    print(pos)

def main():
    arm = robot_start()
    worker2(arm)
    # arm = ""
    """
    threading.Thread(target=worker, args=[arm, ], daemon=True).start()

    xhc.process(
        classification_mode=ClassificationMode.NO_CLASSIFICATION,
        video_index=VIDEO_INDEX,
        robot_command_queue=COMMAND_QUEUE,
        dataset_path=None,
        model_path=None
    )

    COMMAND_QUEUE.join()
    """

if __name__ == "__main__":
    main()
