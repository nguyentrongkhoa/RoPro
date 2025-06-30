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
dxl.establish_connection(device_name = '/dev/cu.usbserial-FT5WIPF3')

# Specify the motor IDs - these need to be set for each motor separately using the Dinamixel-Wizzard program before running this script.
motor_ids        = [1, 2]

# We want to control the motors by setting the electric current. The following operating modes are available:
# CURRENT_CONTROL_MODE, VELOCITY_CONTROL_MODE, POSITION_CONTROL_MODE, EXTENDED_POSITION_CONTROL_MODE, CURRENT_POSITION_CONTROL_MODE, PWM_CONTROL_MODE
#dxl.set_operating_mode(motor_ids, CURRENT_POSITION_CONTROL_MODE)


time_duration = 10 # [seconds]

q_start   = dxl.get_pos(motor_ids)[0]     # get current motor position 
q_thresh  = 1                             # threshold of motor position displacement before recognizing contact
t_start   = time.time()                   # get current system time
contact_detected = False                  # this variable will be set to True in case of contact



# Do the following for <time_duration> amount of time
while (time.time() - t_start) < time_duration:

    # get current motor position
    q_curr = dxl.get_pos(motor_ids)[0]
    
    # has the motor position changed beyond threshold?
    if abs(q_start - q_curr) > q_thresh:
        contact_detected = True
        break
    # --
# --


# print out whether there was a contact
if contact_detected:
    print('There was a contact!')
else:
    print('There was no contact!')



# Tell the motors to stop 
dxl.set_torque_enabled(motor_ids, False)

# Disconnect from dynamixel motors.
# If we de not properly disconnect from the Dynamixel motors before this Python script has ended,
# establishing a connection could fail in the future. If this happens, we need to restart the Dynamixel motors.
dxl.disconnect()