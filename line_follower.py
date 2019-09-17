###############################################
##               LIBARY IMPORT               ##
###############################################
from ev3dev2.motor import LargeMotor, MediumMotor
from ev3dev2.port import OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2

###############################################
##              I/O DEFINING               ##
###############################################
i_cs_r    = ColorSensor(INPUT_1)
i_cs_l    = ColorSensor(INPUT_2)

o_wheel_r = LargeMotor(OUTPUT_A)
o_wheel_l = LargeMotor(OUTPUT_B)
o_lift    = MediumMotor(OUTPUT_C)

