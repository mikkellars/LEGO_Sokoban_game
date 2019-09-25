from controller import line_follower, play_music
from timeit import default_timer as timer
from ev3dev2.button import Button
import time as t

count = 0
btn = Button()

number = 0
#play_music.imerial()
t1 = timer()
t2 = timer()
suspend = False
while 1:
    # Exit
    if btn.any():
        exit()

    # Line follower
    t2 = timer()
    if line_follower.intersection() is True and (t2 - t1) > 1:
        number = number + 1
        print(number)
        t1 = timer()
        suspend = True     
        
    line_follower.follow(suspend)
    
    if suspend is True:
        line_follower.stop()
        play_music.sound()
        t.sleep(2)
        #line_follower.run_forward(1)
        #line_follower.turn_left()
        line_follower.turn_backward()
        suspend = False

    # Print
    # count + 1
    # if count % 1000000000 == 0:
    #     line_follower.print_color_values()
    #     count = 0

