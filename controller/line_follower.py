""" MOTOR CONTROL MODULE """

###############################################
##               LIBARY IMPORT               ##
###############################################
#import main
from timeit import default_timer as timer
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D, MoveTank, SpeedPercent, MoveSteering
from ev3dev2.sensor.lego import ColorSensor, LightSensor
from ev3dev2.sensor import INPUT_4, INPUT_1, INPUT_2

from ev3dev2.sound import Sound
###############################################
##                I/O DEFINING               ##
###############################################
# Color sensor
i_cs_r          = ColorSensor(INPUT_4)
i_cs_l          = ColorSensor(INPUT_1)

# Light sensor
i_ls          = LightSensor(INPUT_2)

# Large motor
o_wheel_l       = LargeMotor(OUTPUT_A)
o_wheel_r       = LargeMotor(OUTPUT_B)
o_both_wheel    = MoveTank(OUTPUT_A, OUTPUT_B)
o_both_steering = MoveSteering(OUTPUT_A, OUTPUT_B)
#o_lift       = MediumMotor(OUTPUT_B)

###############################################
##              GLOBAL VARIABLES             ##
###############################################
# Follow line
CS_SCALE = 1 # OPTIMAL SETTING 2
CS_BIAS = 20

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

def follow(cargo):
    """
    Follows a line and changes the state to controller if an intersection is reached
    """
    
    global CS_SCALE
    global CS_BIAS
    
    new_state = "follow"
    txt = ""

    speed_cs_r = i_cs_r.reflected_light_intensity / CS_SCALE
    speed_cs_l = i_cs_l.reflected_light_intensity / CS_SCALE
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
        new_state = "ctrl"
        txt = "Reached intersection"
    
    return (new_state, txt)

def print_color_values():
    print("Left color sensor value: " + str(i_cs_r.reflected_light_intensity))
    print("Right color sensor value: " + str(i_cs_l.reflected_light_intensity))

def intersection():
    """Detects intersections and returns true if one is spotted"""
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
    o_both_wheel.on_for_seconds(40, 40, 0.2, False) # OPTIMAL VALUE 10, 10, 1

def run_backward():
    """Makes the robot go backwards over intersection"""
    o_both_wheel.on_for_seconds(-10, -10, 1.25)

def stop():
    """Stops the robot"""
    o_wheel_l.command = LargeMotor.COMMAND_STOP
    o_wheel_r.command = LargeMotor.COMMAND_STOP

def turn_left():
    """Turns the robot to the left"""
    o_both_wheel.on_for_seconds(40, 40, 0.35, False)
    o_both_steering.on_for_rotations(-100, SpeedPercent(40), 0.5)  # OPTIMAL VALUE 0.5

def turn_right():
    """Turns the robot to the right"""
    o_both_wheel.on_for_seconds(40, 40, 0.35, False)   
    o_both_steering.on_for_rotations(100, SpeedPercent(40), 0.5)  # OPTIMAL VALUE 0.5

def turn():
    """Turns the robot 180 degrees"""
    o_both_steering.on_for_rotations(100, SpeedPercent(40), 1.1) # OPTIMAL VALUE 1

def follow_backwards(cargo):
    """Makes the robot drive backwards towards intersection"""
    new_state = "follow backwards"
    txt = ""

    speed_cs_r = -i_cs_r.reflected_light_intensity / 5
    speed_cs_l = -i_cs_l.reflected_light_intensity / 5
    
    # # Sharp corner add-on
    # if i_cs_r.reflected_light_intensity < 10 and i_cs_r.reflected_light_intensity != 0:
    #     speed_cs_r = 10
    # if i_cs_l.reflected_light_intensity < 10 and i_cs_l.reflected_light_intensity != 0:
    #     speed_cs_l = 10
    
    o_wheel_l.duty_cycle_sp =  speed_cs_r 
    o_wheel_r.duty_cycle_sp =  speed_cs_l 
    print(o_wheel_l.duty_cycle_sp)
    print(o_wheel_r.duty_cycle_sp)
    o_wheel_l.command = LargeMotor.COMMAND_RUN_DIRECT
    o_wheel_r.command = LargeMotor.COMMAND_RUN_DIRECT

    # if intersection() is True:
    #     new_state = "ctrl"
    #     txt = "Reached intersection"
    
    return (new_state, txt)

def follow_turn():
    """Follows a line and changes the state to controller if an intersection is reached"""
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