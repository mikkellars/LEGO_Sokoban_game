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
# CS_SCALE = 1 # OPTIMAL SETTING 1.1
# CS_BIAS = 10
SPEED_REDUCTION = 45
MAX_SPEED = 90

# Intersection
DETECT_INTER_DELAY = 0.6
T1_CS_INTERSECTION = 100
T2_CS_INTERSECTION = 0

# Intersection2
LS_THRESH = 50

###############################################
##                FUNCTIONS                  ##
###############################################

def turn_left2():
    o_both_wheel.on_for_seconds(43, 43, 0.35, False)
    
    turn_right_sensor = True
    while turn_right_sensor:
        if i_cs_r.reflected_light_intensity < 12:
            turn_right_sensor = False
        
        o_wheel_l.duty_cycle_sp = 0
        o_wheel_r.duty_cycle_sp = 40
        o_wheel_l.command = LargeMotor.COMMAND_RUN_DIRECT
        o_wheel_r.command = LargeMotor.COMMAND_RUN_DIRECT

    o_wheel_l.duty_cycle_sp = 0
    o_wheel_r.duty_cycle_sp = 0
    o_wheel_l.command = LargeMotor.COMMAND_RUN_DIRECT
    o_wheel_r.command = LargeMotor.COMMAND_RUN_DIRECT


def intersection2():
    global LS_THRESH
    global i_ls

    result = False
    if i_ls.reflected_light_intensity < LS_THRESH:
        result = True
    return result

def follow():
    """
    Follows a line and changes the state to controller if an intersection is reached
    """
    global i_cs_r
    global i_cs_l
    global o_wheel_r
    global o_wheel_l
    
    global SPEED_REDUCTION
    global MAX_SPEED
    
    i_cs_r_val = i_cs_r.reflected_light_intensity
    i_cs_l_val = i_cs_l.reflected_light_intensity

    if i_cs_r_val == 0:
        i_cs_r_val = 1
    if i_cs_l_val == 0:
        i_cs_l_val = 1

    speed_cs_l = MAX_SPEED - (1 - (i_cs_l_val / (i_cs_l_val + i_cs_r_val))) * SPEED_REDUCTION
    speed_cs_r = MAX_SPEED - (1 - (i_cs_r_val / (i_cs_l_val + i_cs_r_val))) * SPEED_REDUCTION

    if speed_cs_l > 100:
        speed_cs_l = 100
    if speed_cs_r > 100:
        speed_cs_r = 100

    o_wheel_l.duty_cycle_sp = speed_cs_l
    o_wheel_r.duty_cycle_sp = speed_cs_r

    o_wheel_l.command = LargeMotor.COMMAND_RUN_DIRECT
    o_wheel_r.command = LargeMotor.COMMAND_RUN_DIRECT

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

###############################################
##              Main function                ##
###############################################
def main():
    time.sleep(2)

    # get sequence
    txtFile = open("sequence.txt", 'r')
    task_seq = txtFile.read()
    txtFile.close()

    # task_seq = "ldruldruldruldruldruldruldru" # ROUND IN CIRCLE
    # task_seq = "UruulDrddlUruulDrddl"
    # task_seq = "llllllll"

    task_seq_list = list(task_seq)

    while(len(task_seq_list) != 0):
        action = task_seq_list.pop(0)
        
        if action == 'u':
            while(intersection2()):
                o_wheel_l.duty_cycle_sp = 75
                o_wheel_r.duty_cycle_sp = 75
                o_wheel_l.command = LargeMotor.COMMAND_RUN_DIRECT
                o_wheel_r.command = LargeMotor.COMMAND_RUN_DIRECT
        elif action == 'l':
            turn_left2()
        elif action == 'r':
            turn_right()
        elif action == 'd':
            turn()
        elif action == 'T':
            run_backward()
            turn()

        result = False
        while not result: # true when intersection
            follow()
            result = intersection2()

    stop()

if __name__ == "__main__":
    main()