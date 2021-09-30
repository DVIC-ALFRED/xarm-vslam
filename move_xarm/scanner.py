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
    """Allow to stop the arm with Ctrl+C during movement"""
    print("\nSIGINT Captured, terminating")
    if arm is not None:
        arm.set_state(4)
        arm.disconnect()
    print(arm)
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

def robot_start() -> XArmAPI:
    """Initialize the robot & move to initial position"""
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

def points_line(pos:float=init_pos,height:int=0,length:int=0, start_angle:int=0,end_angle:int=0, step:int=0)->float:
    """Get points for the lines"""
    pos[2]+=height #change the height of the scanning
    points=[]
    i=0
    while start_angle>=end_angle: #scanning from the first angle until the end_angle
        angle=radians(start_angle) #convert angle in degrees
        move_angle=[pos[0]*cos(angle),pos[0]*sin(angle)]+pos[2:-1]+[pos[-1]+start_angle] # =[x*cosA, x*sinA, z+h, roll, pitch, yaw+A]
        move_angle=[round(elem,2) for elem in move_angle] #round list
        add_pos=[(11+length)*cos(angle),(11+length)*sin(angle),10,0,-7.2,0] #11 & -7.2 are used to move servo n°5 to 75° (normally at 82.2°)
        move_line=list(map(lambda x,y: x+y, move_angle,add_pos)) #add the two coordinates
        move_line=[round(elem,2) for elem in move_line] #round list

        if i%2==0:
            points.append(move_angle)
            points.append(move_line)
        else:
            points.append(move_line)
            points.append(move_angle)
        
        i+=1
        start_angle-=step
    return points

def points_arc(pos:float=init_pos,height:int=0,start_angle:int=0,end_angle:int=0):
    """Get points for the arc"""
    pos[2]+=height #change the height of the scanning
    points=[pos] #add the first position for the height
    for i in range(3):
        
    return points


def scanner_line(arm: XArmAPI,pos:float=init_pos,height:int=0,length:int=0, start_angle:int=0,end_angle:int=0, step:int=0)->None:
    """Move arm in lines"""
    arm_pos = points_line(init_pos,height,length,start_angle,end_angle,step)
    for point in arm_pos:
        arm.set_position(*point,speed=speed,mvacc=mvacc,wait=True)



def main():
    arm = robot_start()
    scanner_line(arm,init_pos,200,300,100,-100,50)

if __name__ == "__main__":
    main()
