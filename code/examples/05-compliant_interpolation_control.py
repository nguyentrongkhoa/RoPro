

# Import functionality that is implemented somewhere else
from dynamixel_port import *                           # communication with Dynamixel motors
import time                                            # handling time
import numpy as np

from linear_interpolation import *


# Create an easy-to-use port to dynamixel motors
dxl = DynamixelPort()

# Before we can talk to the Dynamixel motors, we need to establish a USB connection.
# For this, we need to know the name of the USB device. 
# Example names: Windows: "COM*", Linux: "/dev/ttyUSB*", MacOS: "/dev/tty.usbserial-*"
dxl.establish_connection(device_name = '/dev/cu.usbserial-FT5WIPF3', baudrate=1000000)

# Specify the motor IDs - these need to be set for each motor separately using the Dinamixel-Wizzard program before running this script.
hand_motor_ids = [1, 2]
cntrl_motor_id = [7]
all_motor_ids  = hand_motor_ids + cntrl_motor_id

# We want to control the motors by setting the electric current. The following operating modes are available:
# CURRENT_CONTROL_MODE, VELOCITY_CONTROL_MODE, POSITION_CONTROL_MODE, EXTENDED_POSITION_CONTROL_MODE, CURRENT_POSITION_CONTROL_MODE, PWM_CONTROL_MODE
dxl.set_operating_mode(all_motor_ids, CURRENT_POSITION_CONTROL_MODE)

# Activate motors 
dxl.set_torque_enabled(all_motor_ids, True)


# everything about the keyframe interpolation
kf1       = [0, 200]
kf2       = [1000, 2000]

keyframes = [kf1, kf2]
durations = [1.]
lin       = LinearInterpolation(keyframes, durations)





# move controller to zero configuration
dxl.set_goal_pos(cntrl_motor_id, 0)
time.sleep(2)

# define controlled stiffnesses of motors
dxl.set_goal_current(cntrl_motor_id, [50])
dxl.set_goal_current(hand_motor_ids, [200, 200])

# The variable frac indicates how far we transitioned from the first to the second keyframe. Its value ranges 
# between 0 and 1 where 0 indicates the 100% of the first keyframe and 1 indicates 100% of the second keyframe.
frac = 0

# The bias pushes the signal towards the first keyframe.
# Thus, if we do not press the cntrl, the hand will open.
bias = -0.03


# Do the following until the end of time
while True:

    # get current motor positions
    curr_pos = dxl.get_pos(all_motor_ids, multi_turn=True)
    
    # Compute the discrepency between the cntrl levers target position and its actual position
    delta = 0.0001 * curr_pos[2]

    # update the desired location along the interpolation based on the control lever and the bias
    frac  = frac + delta + bias
    
    # Make sure that the variable frac stays within 0 and 1
    if frac < 0.:
        frac = 0.
    
    if frac > 1.:
        frac = 1.
    
    hand_motor_goal_pos = lin.get_values_for_time(frac).tolist()
    dxl.set_goal_pos(hand_motor_ids, hand_motor_goal_pos)
# --


# Tell the motors to stop 
dxl.set_torque_enabled(all_motor_ids, False)

# Disconnect from dynamixel motors.
# If we de not properly disconnect from the Dynamixel motors before this Python script has ended,
# establishing a connection could fail in the future. If this happens, we need to restart the Dynamixel motors.
dxl.disconnect()