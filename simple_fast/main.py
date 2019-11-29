#!/usr/bin/env micropython
""" MOTOR CONTROL MODULE """

###############################################
##               LIBARY IMPORT               ##
###############################################
from timeit import default_timer as timer
#from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent, MoveSteering
from ev3dev2.sensor.lego import LightSensor
#from ev3dev2.sensor import INPUT_4, INPUT_1, INPUT_2
from ev3fast import *
from ev3dev2.motor import MoveTank
from collections import deque

###############################################
##                I/O DEFINING               ##
###############################################
# Color sensor
i_cs_r          = ColorSensor('in4')
i_cs_l          = ColorSensor('in1')

# Light sensor
i_ls            = LightSensor('in2')

# Large motor
o_wheel_l       = LargeMotor('outA')
o_wheel_r       = LargeMotor('outB')
o_both_wheel    = MoveTank('outA', 'outB')
o_both_steering = MoveSteering('outA', 'outB')

###############################################
##              GLOBAL VARIABLES             ##
###############################################
# Follow line
CS_SCALE = 1 # OPTIMAL SETTING 1.1
CS_BIAS = 10

# Intersection
DETECT_INTER_DELAY = 0.6
T1_CS_INTERSECTION = 100
T2_CS_INTERSECTION = 0

# Intersection2
LS_THRESH = 50

###############################################
##                FUNCTIONS                  ##
###############################################

def intersection2():
    global LS_THRESH
    global i_ls

    result = False
    if i_ls.reflected_light_intensity < LS_THRESH:
        result = True
    return result

def _update_scale():
    """"""
    global LIGHT_INTENSITY_SCALE
    print("left wheel:", o_wheel_l.position)
    print("right wheel:", o_wheel_r.position)

    if o_wheel_l.position > 400 and o_wheel_r.position > 400:
        LIGHT_INTENSITY_SCALE = 2
        o_wheel_l.position = 99
        o_wheel_r.position = 99
    else:
        LIGHT_INTENSITY_SCALE = 1

def follow():
    """
    Follows a line and changes the state to controller if an intersection is reached
    """
    global i_cs_r
    global i_cs_l
    global o_wheel_r
    global o_wheel_l

    global CS_SCALE
    global CS_BIAS
    
    speed_cs_r = i_cs_r.reflected_light_intensity / CS_SCALE 
    speed_cs_l = i_cs_l.reflected_light_intensity / CS_SCALE 

    if speed_cs_l > 100:
        speed_cs_l = 100
    if speed_cs_r > 100:
        speed_cs_r = 100


    # speed_cs_r += CS_BIAS
    # speed_cs_l += CS_BIAS
    
    # if i_cs_r.reflected_light_intensity < 10 and i_cs_r.reflected_light_intensity != 0:
    #     speed_cs_r = -20
    # if i_cs_l.reflected_light_intensity < 10 and i_cs_l.reflected_light_intensity != 0:
    #     speed_cs_l = -20

    o_wheel_l.duty_cycle_sp = speed_cs_l
    o_wheel_r.duty_cycle_sp = speed_cs_r
    o_wheel_l.command = LargeMotor.COMMAND_RUN_DIRECT
    o_wheel_r.command = LargeMotor.COMMAND_RUN_DIRECT

    # if intersection() is True:
    #     new_state = "ctrl"
    #     txt = "Reached intersection"
    if intersection2() is True:
        return True

    return False

def intersection():
    """Detects intersections and returns true if one is spotted"""
    global i_cs_r
    global i_cs_l

    global T1_CS_INTERSECTION
    global T2_CS_INTERSECTION
    global DETECT_INTER_DELAY

    result = False

    if i_cs_l.reflected_light_intensity < 12 and i_cs_l.reflected_light_intensity != 0:
        T1_CS_INTERSECTION = timer()
        # cs_l_val = i_cs_l.reflected_light_intensity

    if i_cs_r.reflected_light_intensity < 12 and i_cs_r.reflected_light_intensity != 0:
        T2_CS_INTERSECTION = timer()
        # cs_r_val = i_cs_r.reflected_light_intensity

    if abs(T1_CS_INTERSECTION - T2_CS_INTERSECTION) < DETECT_INTER_DELAY:
        T1_CS_INTERSECTION = 100
        T2_CS_INTERSECTION = 0
        result = True
        # print("Left color sensor value: " + str(cs_l_val))
        # print("Right color sensor value: " + str(cs_r_val))

    return result

def run_forward():
    """Makes the robot go over intersection"""
    global o_both_wheel
    o_both_wheel.on_for_seconds(40, 40, 0.35, False) # OPTIMAL VALUE 10, 10, 1

def run_backward():
    """Makes the robot go backwards over intersection"""
    global o_both_wheel
    o_both_wheel.on_for_seconds(-40, -40, 0.35)

def stop():
    """Stops the robot"""
    global o_both_wheel
    o_both_wheel.on_for_seconds(1, 1, 0.1, True)

def turn_left():
    """Turns the robot to the left"""
    global o_both_wheel
    global o_both_steering

    o_both_wheel.on_for_seconds(43, 43, 0.35, False)
    o_both_steering.on_for_rotations(-100, SpeedPercent(40), 0.5)  # OPTIMAL VALUE 0.5

def turn_right():
    """Turns the robot to the right"""
    global o_both_wheel
    global o_both_steering
    
    o_both_wheel.on_for_seconds(43, 43, 0.35, False)   
    o_both_steering.on_for_rotations(100, SpeedPercent(40), 0.5)  # OPTIMAL VALUE 0.5

def turn():
    """Turns the robot 180 degrees"""
    global o_both_steering

    o_both_steering.on_for_rotations(100, SpeedPercent(40), 1) # OPTIMAL VALUE 1

def follow_backwards():
    """Makes the robot drive backwards towards intersection"""
    global o_wheel_r
    global o_wheel_l

    speed_cs_r = -i_cs_r.reflected_light_intensity / 5
    speed_cs_l = -i_cs_l.reflected_light_intensity / 5
    
    # # Sharp corner add-on
    # if i_cs_r.reflected_light_intensity < 10 and i_cs_r.reflected_light_intensity != 0:
    #     speed_cs_r = 10
    # if i_cs_l.reflected_light_intensity < 10 and i_cs_l.reflected_light_intensity != 0:
    #     speed_cs_l = 10
    
    o_wheel_l.duty_cycle_sp =  speed_cs_r 
    o_wheel_r.duty_cycle_sp =  speed_cs_l 
    o_wheel_l.command = LargeMotor.COMMAND_RUN_DIRECT
    o_wheel_r.command = LargeMotor.COMMAND_RUN_DIRECT

    # if intersection() is True:
    #     new_state = "ctrl"
    #     txt = "Reached intersection"
    
def follow_turn():
    """Follows a line and changes the state to controller if an intersection is reached"""
    global o_wheel_l
    global o_wheel_r

    speed_cs_r = i_cs_r.reflected_light_intensity / 2
    speed_cs_l = i_cs_l.reflected_light_intensity / 2 
    # Sharp corner add-on
    if i_cs_r.reflected_light_intensity < 10 and i_cs_r.reflected_light_intensity != 0:
        speed_cs_r = -20
    if i_cs_l.reflected_light_intensity < 10 and i_cs_l.reflected_light_intensity != 0:
        speed_cs_l = -20
    o_wheel_l.duty_cycle_sp = speed_cs_l
    o_wheel_r.duty_cycle_sp = speed_cs_r
    o_wheel_l.command = LargeMotor.COMMAND_RUN_DIRECT
    o_wheel_r.command = LargeMotor.COMMAND_RUN_DIRECT

    return intersection()



###############################################
##              Main function                ##
###############################################
def main():

    # get sequence
    # task_seq = "uldruldruldruldruldr"
    txtFile = open("sequence.txt", 'r')
    task_seq = txtFile.read()
    txtFile.close()

   # task_seq = "ldruldruldruldruldruldruldru" # ROUND IN CIRCLE
   # task_seq = "UruulDrddlUruulDrddl"
   # task_seq = "uuuuuuuuuu";
    # translate sequence to behaviors
    # print(task_seq)

    task_seq_list = list(task_seq)
    
    time.sleep(2)

    while(len(task_seq_list) != 0):
        action = task_seq_list.pop(0)
        next_action = task_seq_list[0]
        if action == 'u':
            if next_action == 'u':
                while(intersection2()):
                    o_both_wheel.on_for_seconds(100, 100, 0.5, False, False)
            else:
                run_forward()
        elif action == 'l':
            turn_left()
        elif action == 'r':
            turn_right()
        elif action == 'd':
            turn()
        elif action == 'T':
            run_backward()
            turn()

        result = False
        while not result: # true when intersection
            result = follow()
    stop()

if __name__ == "__main__":
    main()