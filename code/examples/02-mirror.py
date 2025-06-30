# Import functionality that is implemented somewhere else
from dynamixel_port import *                           # communication with Dynamixel motors
import time                                            # handling time


# Create an easy-to-use port to dynamixel motors
dxl = DynamixelPort()

# Before we can talk to the Dynamixel motors, we need to establish a USB connection.
# For this, we need to know the name of the USB device. 
# Example names: Windows: "COM*", Linux: "/dev/ttyUSB*", MacOS: "/dev/tty.usbserial-*"
dxl.establish_connection(device_name = '/dev/cu.usbserial-FT5WIPF3', baudrate=1000000)
#dxl.establish_connection(device_name = '/dev/cu.usbserial-2')

# Specify the motor IDs - these need to be set for each motor separately using the Dinamixel-Wizzard program before running this script.
motor_ids        = [7, 2]

# We want to control the motors by setting the electric current. The following operating modes are available:
# CURRENT_CONTROL_MODE, VELOCITY_CONTROL_MODE, POSITION_CONTROL_MODE, EXTENDED_POSITION_CONTROL_MODE, CURRENT_POSITION_CONTROL_MODE, PWM_CONTROL_MODE
dxl.set_operating_mode(motor_ids, CURRENT_POSITION_CONTROL_MODE)


# Tell the motors to stop 
dxl.set_torque_enabled(motor_ids, True)

time_duration = 10000         # in seconds
t_start       = time.time()   # get current system time

dxl.set_goal_pos(motor_ids, 0)
time.sleep(2)


dxl.set_goal_current(motor_ids, [0, 300])

# Do the following for <time_duration> amount of time
while (time.time() - t_start) < time_duration:

    # get current motor position
    curr_pos = dxl.get_pos(motor_ids, multi_turn=True)
    print(curr_pos)
    dxl.set_goal_pos(motor_ids, [curr_pos[0], curr_pos[0]])

# --

# Tell the motors to stop 
dxl.set_torque_enabled(motor_ids, False)

# Disconnect from dynamixel motors.
# If we de not properly disconnect from the Dynamixel motors before this Python script has ended,
# establishing a connection could fail in the future. If this happens, we need to restart the Dynamixel motors.
dxl.disconnect()