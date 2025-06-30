# Import functionality that is implemented somewhere else
from dynamixel_port import *                           # communication with Dynamixel motors
import time                                            # handling time
import numpy as np



# Create an easy-to-use port to dynamixel motors
dxl = DynamixelPort()

# Before we can talk to the Dynamixel motors, we need to establish a USB connection.
# For this, we need to know the name of the USB device. 
# Example names: Windows: "COM*", Linux: "/dev/ttyUSB*", MacOS: "/dev/tty.usbserial-*"
dxl.establish_connection(device_name = '/dev/cu.usbserial-FT5WIPF3', baudrate=1000000)

# Specify the motor IDs - these need to be set for each motor separately using the Dinamixel-Wizzard program before running this script.
motor_ids        = [1, 2, 3, 4, 5, 6]



# We want to control the motors by setting the electric current. The following operating modes are available:
# CURRENT_CONTROL_MODE, VELOCITY_CONTROL_MODE, POSITION_CONTROL_MODE, EXTENDED_POSITION_CONTROL_MODE, CURRENT_POSITION_CONTROL_MODE, PWM_CONTROL_MODE
dxl.set_operating_mode(motor_ids, CURRENT_POSITION_CONTROL_MODE)


# Tell the motors to stop 
dxl.set_torque_enabled(motor_ids, True)

kf_open   = [2078, 3378, 3663, 2073, 571, 825]

goal_pos = dxl.get_pos(motor_ids)


amplitude = 1000
start_time = time.time()
while True:

    time_in_loop  = 1. * time.time() - start_time
    time_factor   = 1
    add_value     =  (amplitude / 2.) * (1. + np.sin(time_factor * time_in_loop))
    
    goal_value    = np.array(np.array(kf_open) + np.ones(len(kf_open)) * add_value).astype(int)
    goal_value[4] = 571  # thumb stays where it is

    print(goal_value)
    dxl.converge_to_pos(motor_ids, goal_value.tolist(), gain=0.1, current=300)
# - while



# Tell the motors to stop 
dxl.set_torque_enabled(motor_ids, False)

# Disconnect from dynamixel motors.
# If we de not properly disconnect from the Dynamixel motors before this Python script has ended,
# establishing a connection could fail in the future. If this happens, we need to restart the Dynamixel motors.
dxl.disconnect()