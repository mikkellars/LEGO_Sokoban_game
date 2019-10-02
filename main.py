""" MAIN MODULE """

###############################################
##               LIBARY IMPORT               ##
###############################################
from state_machine import state_machine
from controller import line_follower, play_music
from timeit import default_timer as timer
from ev3dev2.button import Button
import time

def main():
    m = state_machine()
    m.add_state("line follower", line_follower)
    m.add_state("finish", None, end_state=1)
    m.run(False)

    # btn = Button()
    # t1 = timer()
    # t2 = timer()
    # suspend = False
    # #number = 0

    # while 1:
    #     # Exit
    #     if btn.any():
    #         exit()

    #     # Line follower
    #     t2 = timer()
    #     if line_follower.intersection() is True and (t2 - t1) > 1:
    #         #number = number + 1
    #         #print(number)
    #         t1 = timer()
    #         suspend = True     
            
    #     line_follower.follow(suspend)
        
    #     if suspend is True:
    #         line_follower.stop()
    #        # play_music.sound()

    #         #line_follower.run_forward(1)
    #         #line_follower.turn_left()
    #         line_follower.turn_right()
            
    #         suspend = False

    #     # Print
    #     # count + 1
    #     # if count % 1000000000 == 0:
    #     #     line_follower.print_color_values()
    #     #     count = 0

if __name__ == "__main__":
    main()