from controller import line_follower, play_music
from time import sleep
from ev3dev2.button import Button

count = 0
btn = Button()
intersection_det = False
number = 0
#play_music.imerial()
while 1:
    # Exit
    if btn.any():
        exit()

    # Line follower
    if line_follower.follow(intersection_det) is True:
        number = number + 1
        print(number)
        
    #line_follower.color_follow()
    
    # Print
    # count + 1
    # if count % 1000000000 == 0:
    #     line_follower.print_color_values()
    #     count = 0
    
