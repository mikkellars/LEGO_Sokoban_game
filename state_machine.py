from controller import line_follower, play_music
# from timeit import default_timer as timer
from ev3dev2.button import Button
import time

TASK_SEQ = ""

class state_machine:
    """Finite state machine class"""
    global TASK_SEQ

    def __init__(self):
        """Initialize the finite state machine class"""
        self.handlers = {}
        self.start_state = None
        self.end_states = []
        self.btn = Button()
    
    def add_state(self, name, handler, end_state=0):
        """Adds a state to the finite state machine"""
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.end_states.append(name)
    
    def set_start(self, name):
        """Sets the state as start state"""
        self.start_state = name.upper()
    
    def run(self, cargo):
        """Starts the finite state machine"""
        # make sure the state machine is set up correctly
        try:
            handler = self.handlers[self.start_state]
        except:
            raise Exception("Must call .set_start() before run()")
        if not self.end_states:
            raise Exception("At least one state must be an end_state")
        
        # add dummy char to task sequence
        TASK_SEQ = "S" + cargo
        
        while (True):
            # If button is pressed then stop
            if self.btn.any():
                exit()
            
            (new_state, cargo) = handler(cargo)
            
            if cargo != "":
                print(cargo)
            
            # check if a end states is reaches
            if new_state.upper() in self.end_states:
                print("Reached", new_state)
                line_follower.stop()
                play_music.sound()
                break
            else:
                # if new state is control take next task in task_sequence
                if new_state == "ctrl":
                    TASK_SEQ = TASK_SEQ[1:]
                    cargo = TASK_SEQ
                    print(cargo)

                # change handler to new_state's handler
                handler = self.handlers[new_state.upper()]

def start(cargo):
    """Initial state which changes the state to ctrl."""
    # play_music.sound()
    time.sleep(1)
    # return (keep cargo because it contains task sequence)
    new_state = "ctrl"
    return (new_state, cargo)

def controller(cargo):
    """Controlles which state to go to next depending on the task sequence."""
    new_state = ""
    txt = ""

    if cargo == '':
        new_state = "end"
    else:
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
            new_state = "backward"
            txt = "Going back to previous intersection"
        elif task == 'd':
            new_state = "back"
            txt = "Going backwards"
        else:
            new_state = "end"
    return (new_state, txt)

def forward(cargo):
    """Goes forward and changes the state to follow."""
    # If intersection is reached change state
    line_follower.run_forward()
    print("Running forward")

    # return
    new_state = "follow"
    txt = "follow line.."
    return (new_state, txt)

def left(cargo):
    """Turns the robot to the left and changes the state to follow."""
    # When the robot has turned left change state to follow
    line_follower.turn_left()
    print("Turning left")

    # return
    new_state = "follow"
    txt = "follow line.."
    return (new_state, txt)

def right(cargo):
    """Turns the robot to the right and changes the state to follow."""
    # When the robot has turned right change state to forward
    line_follower.turn_right()
    print("Turning right")
    
    # return
    new_state = "follow"
    txt = "follow line.."
    return (new_state, txt)

def backward(cargo):
    # When the robot has turned 180 degrees change state to forward
    print("Go away from  jewl")
    line_follower.run_backward()

    # return
    new_state = "back"
    txt = ""
    return (new_state, txt)

def back(cargo):
    """Turns the robot 180 degress and then follows the line towards an intersection."""
    # Go backwards
    line_follower.turn()

    # return
    new_state = "follow"
    txt = "follow line.."

    return (new_state, txt)

def stop(cargo):
    """Stops the motors, plays a sound and changes the state to end."""
    # play victory sound
    play_music.sound()
    line_follower.stop()
    # return
    new_state = "end"
    txt = "done!"

    return (new_state, txt)

def follow(cargo):
    """Dummy state for debugging."""
    new_state = "ctrl"
    txt = "reached intersection"

    return (new_state, txt)