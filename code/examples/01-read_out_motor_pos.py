#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This minimal working example shows how to connect to Dynamixel motors via USB and how to control them.
In case you have any doubts or questions, please send an email to Steffen Puhlmann (spuhlmann@bht-berlin.de).
'''


# Import functionality that is implemented somewhere else
from dynamixel_port import *                           # communication with Dynamixel motors
import time                                            # handling time




# Create an easy-to-use port to dynamixel motors
dxl = DynamixelPort()

# Before we can talk to the Dynamixel motors, we need to establish a USB connection.
# For this, we need to know the name of the USB device. 
# Example names: Windows: "COM*", Linux: "/dev/ttyUSB*", MacOS: "/dev/tty.usbserial-*"
dxl.establish_connection(device_name = '/dev/cu.usbserial-FT5WIPF3', baudrate=1000000)


# Specify the motor IDs - these need to be set for each motor separately using the Dinamixel-Wizzard program before running this script.
motor_ids = [2]

# print motor positions of motors whose ID is element of motor_ids to the command line
start_time = time.time()
max_duration = 10 # in seconds

while time.time() - start_time < max_duration:
    print(   dxl.get_pos(motor_ids, multi_turn=True)    )



# Disconnect from dynamixel motors.
# If we de not properly disconnect from the Dynamixel motors before this Python script has ended,
# establishing a connection could fail in the future. If this happens, we need to restart the Dynamixel motors.
dxl.disconnect()