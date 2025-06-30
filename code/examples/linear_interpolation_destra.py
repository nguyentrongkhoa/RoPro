

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


# Tell the motors to stop 
dxl.set_torque_enabled(motor_ids, True)

kf_open   = [2078, 3378, 3663, 2073, 571, 825]
kf_closed = [3700, 5300, 5500, 4000, 571, 2700]
keyframes = [kf_open, kf_closed, kf_open]
durations = [5., 3]


dxl.execute_compliant_interpolation(motor_ids, keyframes, durations, current=200, reset=True, reset_duration=2)

# Tell the motors to stop 
dxl.set_torque_enabled(motor_ids, False)

# Disconnect from dynamixel motors.
# If we de not properly disconnect from the Dynamixel motors before this Python script has ended,
# establishing a connection could fail in the future. If this happens, we need to restart the Dynamixel motors.
dxl.disconnect()