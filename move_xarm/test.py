import signal
import time
from queue import Queue
from typing import final
import sys

import numpy as np

from xarm.wrapper import XArmAPI


VIDEO_INDEX=4
ARM_IP = "172.21.72.200"

speed=40
mvacc=100

arm: XArmAPI = None

def sigint_handler(sig, frame):
    print("\nSIGINT Captured, terminating")
    if arm is not None:
        arm.set_state(4)
        arm.disconnect()

    print(arm)
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

def robot_start() -> XArmAPI:
    global arm
    arm = "dumy"

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
    arm.set_position(*init_pos,
        radius=-1, is_radian=False, wait=True, speed=speed*2.5, mvacc=mvacc, relative=False)

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

def move_arm_line(arm: XArmAPI, goal_pos=[0]*6,speed=None, mvacc=None,wait=False):
    pos=arm.position
    final_pos=[x + y for x, y in zip(pos, goal_pos)]
    arm.set_position(*final_pos,speed=speed,mvacc=mvacc,wait=wait)

def test1(arm: XArmAPI):
    arm.set_servo_angle(1,100,speed=speed,mvacc=mvacc,relative=True, wait=True)
    arm.set_position(z=200,speed=speed,mvacc=mvacc,relative=True,wait=True)
    arm.set_tool_position(x=350,speed=speed,mvacc=mvacc,relative=True,wait=True)
    #arm.set_position(y=100,speed=speed,mvacc=mvacc,relative=True,wait=True)
    arm.set_servo_angle(servo_id=5,angle=30,speed=speed,mvacc=mvacc, wait=True,is_radian=False)

def main():
    arm = robot_start()
    test1(arm)

if __name__ == "__main__":
    main()
