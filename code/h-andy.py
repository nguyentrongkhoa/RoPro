from dynamixel_port import *
from pynput import keyboard 
import time
import threading

# TODO: in order for this program to work properly, please make sure to close the Dynamixel Wizard
# TODO: remap all the motor IDs shown in the Dynamixel Wizard to 1-5 (or 1-4 depending on the number of motors)
# TODO: install the package pynput: pip install pynput

# TODO: to make sure the motors function properly, press S in the beginning to disable all torques. 
# NOTE: make sure to disable the motors when switching operation mode (by pressing S when the motors are already appended to the queue)
# NOTE: only use current control, extended position control and velocity control, everything else is useless

"""
This program is used to command dynamixel motors from the keyboard without any hassle. The following keys are binded
and grouped into 4 types of actions:

Type 1: adding/removing motors to control using their IDs
    1-5: adding the corresponding motors to the list
    R: remove all motors from the list

Type 2: setting operating mode
    C: current control mode
    V: velocity control mode
    P: position control mode
    E: extended position control mode (with multi-turn)
    B: both current and position control mode (also with multi-turn according to the doc)
    M: PWM/Voltage control mode
IMPORTANT: For the control of the hand, only B will be used

Type 3: setting goals for the motors 
    UP: increase the current by CURRENT_INCREMENT
    DOWN: decrease the current by CURRENT_INCREMENT
    SPACEBAR: reset all currents to 0 mA
    RIGHT: increase the position by POSITION_INCREMENT
    LEFT: decrease the position by POSITION_INCREMENT

Type 4: everything else
    S: disable motor torques so that the motors won't impede movements when current or position commands are sent
    D: disconnect all the motors and terminate the entire program
"""

# TODO: change these when working on a new computer
DEVICE_NAME = 'COM10' # COM10 on Tom's computer, COM3 on Max's
BAUD_RATE = 1000000 # will be 1000000 most of the time 

# these constants define how sensitive the control is
# for example, when CURRENT_INCREMENT = 50mA, each arrow key press will add/subtract 50mA from the current value
# NOTE: experiment with these
CURRENT_INCREMENT = 50 # mA
POSITION_INCREMENT = 4096 # 4096 is a full revolution

# helper function
def add_const_to_list(c, l):
    result = [x+c for x in l]
    return result

dxl = DynamixelPort()

# Before we can talk to the Dynamixel motors, we need to establish a USB connection.
# For this, we need to know the name of the USB device. 
# Example names: Windows: "COM*", Linux: "/dev/ttyUSB*", MacOS: "/dev/tty.usbserial-*"
dxl.establish_connection(device_name = DEVICE_NAME, baudrate=BAUD_RATE)

should_disconnect = False
motor_ids_to_control = list() # set instead of list to avoid repetitions
control_mode = -1 # only applies to the motors in the set

def on_release(key):
    global dxl, should_disconnect, motor_ids_to_control, control_mode
    try:
        global CURRENT_INCREMENT, POSITION_INCREMENT
        # if a number is pressed, this will be interpreted as a motor ID
        if key.char in {'1', '2', '3', '4', '5'}:
            motor_ids_to_control.append(int(key.char))
            print(f"Motor {key.char} was added – the queue now consisted of the motors {motor_ids_to_control}")

        # if one of the keys below is pressed, change control mode of all motors in motor_ids_to_control
        # for more info regarding control modes, please consult dynamixel_port-API-documentation in this folder
        elif key.char.upper() == 'C': # current/torque control
            dxl.set_operating_mode(motor_ids_to_control, 0)
            control_mode = 0
            print(f"Motors {motor_ids_to_control} are now in current control mode")
        elif key.char.upper() == 'V': # velocity control
            dxl.set_operating_mode(motor_ids_to_control, 1)
            control_mode = 1
            print(f"Motors {motor_ids_to_control} are now in velocity control mode")
        elif key.char.upper() == 'P': # position control
            dxl.set_operating_mode(motor_ids_to_control, 3)
            control_mode = 3
            print(f"Motors {motor_ids_to_control} are now in position control mode")
        elif key.char.upper() == 'E': # extended position control (multi-turn)
            dxl.set_operating_mode(motor_ids_to_control, 4)
            control_mode = 4
            print(f"Motors {motor_ids_to_control} are now in extended position control mode")
        elif key.char.upper() == 'B': # both, i.e current/torque AND position
            dxl.set_operating_mode(motor_ids_to_control, CURRENT_POSITION_CONTROL_MODE)
            control_mode = 5
            print(f"Motors {motor_ids_to_control} are now in current-based position control mode")
        elif key.char.upper() == 'M': # PWM/Voltage control
            dxl.set_operating_mode(motor_ids_to_control, 16)
            control_mode = 16
            print(f"Motors {motor_ids_to_control} are now in PWM control mode")

        elif key.char.upper() == 'S': # stop motors
            dxl.set_torque_enabled(motor_ids_to_control, False)
            print(f'Motors {motor_ids_to_control} disabled')
        
        # remove all motor ids 
        # since the key C is already used, R is used in this case
        elif key.char.upper() == 'R':
            motor_ids_to_control = []
            print('Queue cleared')
        
        elif key.char.upper() == 'D':
            should_disconnect = True
            dxl.disconnect()
            print('Disconnected from dynamixel motors')
    except AttributeError:
        global CURRENT_INCREMENT, POSITION_INCREMENT
        # Handle special keys like arrow keys.
        # NOTE: if special keys are put in the try block and not the except block, they will not be detected

        # send goal values to the motors (be it current, position etc) using arrow keys
        # UP and DOWN and SPACEBAR are only used for current
        # LEFT and RIGHT are used for position, velocity etc

        # current control
        if key == keyboard.Key.up:
            current_now = dxl.get_current(motor_ids_to_control)
            print(f'Current current in mA: {current_now}')
            goal_current = add_const_to_list(CURRENT_INCREMENT, current_now)
            dxl.set_torque_enabled(motor_ids_to_control)
            dxl.set_goal_current(motor_ids_to_control, goal_current)
            print(f'Motor {motor_ids_to_control} currents increased to {goal_current} mA')
        elif key == keyboard.Key.down:
            current_now = dxl.get_current(motor_ids_to_control)
            goal_current = add_const_to_list(-CURRENT_INCREMENT, current_now)
            dxl.set_torque_enabled(motor_ids_to_control)
            dxl.set_goal_current(motor_ids_to_control, goal_current)
            print(f'Motor {motor_ids_to_control} currents decreased to {goal_current} mA')
        # reset all currents to 0, i.e stop all motors
        elif key == keyboard.Key.space:
            goal_current = [0] * len(motor_ids_to_control)
            dxl.set_torque_enabled(motor_ids_to_control)
            dxl.set_goal_current(motor_ids_to_control, goal_current)
            print(f'Motor {motor_ids_to_control} currents decreased to {goal_current} mA')

        # position, velocity etc    
        elif key == keyboard.Key.right:
            pos_now = dxl.get_pos(motor_ids_to_control, multi_turn=True)
            print(f'Current position: {pos_now}')
            goal_pos = add_const_to_list(POSITION_INCREMENT, pos_now)
            dxl.set_torque_enabled(motor_ids_to_control, True)
            dxl.set_goal_pos(motor_ids_to_control, goal_pos)
            print(f'Motor {motor_ids_to_control} moved to {goal_pos}')
            goal_current = [0] * len(motor_ids_to_control)
            dxl.set_goal_current(motor_ids_to_control, goal_current)
        elif key == keyboard.Key.left:
            pos_now = dxl.get_pos(motor_ids_to_control, multi_turn=True)
            print(f'Current position: {pos_now}')
            goal_pos = add_const_to_list(-POSITION_INCREMENT, pos_now)
            print(goal_pos)
            dxl.set_torque_enabled(motor_ids_to_control, True)
            dxl.set_goal_pos(motor_ids_to_control, goal_pos)
            print(f'Motor {motor_ids_to_control} moved to {goal_pos}')
            goal_current = [0] * len(motor_ids_to_control)
            dxl.set_goal_current(motor_ids_to_control, goal_current)

def start_keyboard_listener():
    listener = keyboard.Listener(on_release=on_release)
    listener.start()  # Non-blocking
    print('Keyboard listener has been started')
    return listener

# Start keyboard listener in a separate thread so that it does not block the main program 
listener_thread = threading.Thread(target=start_keyboard_listener)
listener_thread.daemon = True
listener_thread.start()

# main program
while not should_disconnect:
    pass