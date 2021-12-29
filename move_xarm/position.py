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

    return arm


def main():
    arm = robot_start()
    print(arm.position)

if __name__ == "__main__":
    main()
