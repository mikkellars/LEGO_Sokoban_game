###############################################
##               LIBARY IMPORT               ##
###############################################
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2

###############################################
##                I/O DEFINING               ##
###############################################
i_cs_r       = ColorSensor(INPUT_1)
i_cs_l       = ColorSensor(INPUT_2)

o_wheel_r    = LargeMotor(OUTPUT_A)
o_wheel_l    = LargeMotor(OUTPUT_B)
o_both_wheel = MoveTank(OUTPUT_A, OUTPUT_B)
o_lift       = MediumMotor(OUTPUT_C)

###############################################
##                 FUNCTION                  ##
###############################################

def follow():
    print("Left color sensor value: " + i_cs_r.reflected_light_intensity())
    print("Right color sensor value: " + i_cs_l.reflected_light_intensity())

    o_both_wheel.run_forever(SpeedPercent(i_cs_r.reflected_light_intensity()), SpeedPercent(i_cs_l.reflected_light_intensity()))
    

    