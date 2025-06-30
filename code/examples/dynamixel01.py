from dynamixel_port import *
import time                       # access current system time




dxl = DynamixelPort()


dxl.establish_connection(device_name='/dev/cu.usbserial-FT3FQ3NY')

motor_ids = [5]


start_time   = time.time()  # in seconds
max_duration = 10           # in seconds

time_is_not_up_yet = True

while time_is_not_up_yet:
    
    motor_pos = dxl.get_pos(motor_ids, multi_turn=True)
    print(motor_pos)
    print(motor_pos[0] % 4095)


    time_inside_loop = time.time() - start_time
    if time_inside_loop > max_duration:
        time_is_not_up_yet = False



dxl.disconnect()

