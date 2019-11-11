from controller import line_follower, play_music
# from timeit import default_timer as timer
from ev3dev2.button import Button
import time

TASK_SEQ = ""

class state_machine:
    global TASK_SEQ

    def __init__(self):
        self.handlers = {}
        self.start_state = None
        self.end_states = []
        self.btn = Button()
    
    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.end_states.append(name)
    
    def set_start(self, name):
        self.start_state = name.upper()
    
    def run(self, cargo):
        try:
            handler = self.handlers[self.start_state]
        except:
            raise Exception("Must call .set_start() before run()")
        
        if not self.end_states:
            raise Exception("At least one state must be an end_state")

        TASK_SEQ = cargo

        while (True):
            # If button is pressed => stop
            if self.btn.any():
                exit()
            
            (new_state, cargo) = handler(cargo)
            
            print(cargo)

            if new_state.upper() in self.end_states:
                print("Reached ", new_state)
                break
            else:
                if new_state == "controller":
                    TASK_SEQ = TASK_SEQ[1:]
                    cargo = TASK_SEQ

                handler = self.handlers[new_state.upper()]

def start(cargo):
    # play_music.sound()
    time.sleep(1)
    new_state = "follow"
    return (new_state, cargo)

def controller(cargo):
    new_state = ""
    txt = ""

    task = cargo[0]
    
    if task == 'u':
        new_state = "forward"
        txt = "Going forward"
    elif task == 'l':
        new_state = "left"
        txt = "Turning left"
    elif task == 'r':
        new_state = "right"
        txt = "Turning right"
    elif task == 'T':
        new_state = "turn"
        txt = "Turning 180 degrees"
    elif task == 'd':
        new_state = "back"
        txt = "Going backwards"
    else:
        line_follower.stop()
        new_state = "finish"
        txt = "Finished all tasks!"
    
    return (new_state, txt)

def forward(cargo):
    new_state = "follow"
    txt = "Running forward"

    # If intersection is reached change state
    line_follower.run_forward()

    return (new_state, txt)

def left(cargo):
    # When the robot has turned left change state to follow
    new_state = "follow"
    txt = "Turning left"

    line_follower.turn_left()

    return (new_state, txt)

def right(cargo):
    # When the robot has turned right change state to forward
    new_state = "follow"
    txt = "Turning right"

    line_follower.turn_right()

    return (new_state, txt)

def turn(cargo):
    new_state = ""
    txt = ""

    # When the robot has turned 180 degrees change state to forward

    return (new_state, txt)

def back(cargo):
    new_state = ""
    txt = ""

    # Go backward

    return (new_state, txt)
