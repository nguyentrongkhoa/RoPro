from dynamixel_port import *                           # communication with Dynamixel motors
import time                                            # handling time


dxl = DynamixelPort()

motor_ids        = [7, 2]

dxl.establish_connection(device_name = '/dev/cu.usbserial-FT5WIPF3', baudrate=1000000)
dxl.set_operating_mode(motor_ids, CURRENT_POSITION_CONTROL_MODE)
dxl.set_torque_enabled(motor_ids, True)

goal_pos = 0
dxl.set_goal_pos(motor_ids, goal_pos)

dxl.set_goal_current([7], 50)   # DO NOT USE 1000 !!! (but below 500)


start_time = time.time()
while time.time() - start_time < 20:


    speed = goal_pos - dxl.get_pos([7], multi_turn=True)[0]

    new_goal_pos_of_controlled_motor = dxl.get_pos([2], multi_turn=True)[0] + speed

    dxl.set_goal_pos([2], new_goal_pos_of_controlled_motor)

