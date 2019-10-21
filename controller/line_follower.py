###############################################
##               LIBARY IMPORT               ##
###############################################
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D, MoveTank, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_4, INPUT_1, INPUT_2

from ev3dev2.sound import Sound
###############################################
##                I/O DEFINING               ##
###############################################
i_cs_r       = ColorSensor(INPUT_4)
i_cs_l       = ColorSensor(INPUT_1)

o_wheel_l    = LargeMotor(OUTPUT_A)
o_wheel_r    = LargeMotor(OUTPUT_B)
o_both_wheel = MoveTank(OUTPUT_A, OUTPUT_B)
#o_lift       = MediumMotor(OUTPUT_B)


###############################################
##                FUNCTIONS                  ##
###############################################
def follow(suspend): # Svag over for lys
    if not suspend:
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


def print_color_values():
    print("Left color sensor value: " + str(i_cs_r.reflected_light_intensity))
    print("Right color sensor value: " + str(i_cs_l.reflected_light_intensity))

def intersection():
    result = False
    if  i_cs_r.reflected_light_intensity < 10 and i_cs_r.reflected_light_intensity != 0 and i_cs_l.reflected_light_intensity < 10 and i_cs_l.reflected_light_intensity != 0:
        result = True
    return result

def run_forward(seconds):
   o_both_wheel.on_for_seconds(10,10,seconds)

def stop():
    o_wheel_l.command = LargeMotor.COMMAND_STOP
    o_wheel_r.command = LargeMotor.COMMAND_STOP