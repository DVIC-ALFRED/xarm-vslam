import signal
import time
from queue import Queue
from typing import final
import sys
from math import *

import numpy as np

from xarm.wrapper import XArmAPI


VIDEO_INDEX=4
ARM_IP = "172.21.72.200"

speed=50
mvacc=100
init_pos=[206.9, 0, 258.7, 180, 0,0]

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

    arm.set_position(*init_pos,
        radius=-1, is_radian=False, wait=True, speed=speed*2.5, mvacc=mvacc, relative=False)

    time.sleep(1)
    print("arm started")

    return arm

def move_arm_line(arm: XArmAPI, goal_pos=[0]*6,speed=None, mvacc=None,wait=False):
    pos=arm.position
    final_pos=[x + y for x, y in zip(pos, goal_pos)]
    arm.set_position(*final_pos,speed=speed,mvacc=mvacc,wait=wait)
    
def test1(arm: XArmAPI):
    arm.set_position(z=200,speed=speed,mvacc=mvacc,relative=True,wait=True)
    pos=arm.position
    #print(f"init_pos_z: {pos}")
    arm.set_servo_angle(1,70,speed=speed,mvacc=mvacc,relative=True, wait=True)
    pos=arm.position
    #print(f"move_angle: {pos}")
    arm.set_tool_position(x=350,speed=speed,mvacc=mvacc,relative=True,wait=True)
    #arm.set_position(y=100,speed=speed,mvacc=mvacc,relative=True,wait=True)
    arm.set_servo_angle(servo_id=5,angle=75,speed=speed,mvacc=mvacc, wait=True,is_radian=False)
    pos=arm.position
    print(f"move_line: {pos}")

def points(pos:float=init_pos,height:int=0,length:int=0, start_angle:int=0,end_angle:int=0, step:int=0)->float:
    pos[2]+=height #change the height of the scanning
    points=[pos] #add the first position for the height
    i=0
    while start_angle>=end_angle: #scanning from the first angle until the end_angle
        angle=radians(start_angle)
        move_angle=[pos[0]*cos(angle),pos[0]*sin(angle)]+pos[2:-1]+[pos[-1]+start_angle]
        move_angle=[round(elem,2) for elem in move_angle]
        add_pos=[(11+length)*cos(angle),(11+length)*sin(angle),10,0,-7.2,0] 
        move_line=list(map(lambda x,y: x+y, move_angle,add_pos))
        move_line=[round(elem,2) for elem in move_line]
        if i%2==0:
            points.append(move_angle)
            points.append(move_line)
        else:
            points.append(move_line)
            points.append(move_angle)
        i+=1
        start_angle-=step
    return points

def scanner_line(arm: XArmAPI,pos:float=init_pos,height:int=0,length:int=0, start_angle:int=0,end_angle:int=0, step:int=0):
    arm_pos = points(init_pos,height,length,start_angle,end_angle,step)
    for point in arm_pos:
        arm.set_position(*point,speed=speed,mvacc=mvacc,wait=True)

def main():
    arm = robot_start()
    #test1(arm)
    worker(arm,init_pos,100,350,100,80,20)

if __name__ == "__main__":
    main()
