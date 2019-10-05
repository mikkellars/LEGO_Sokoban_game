""" MAIN MODULE """

###############################################
##               LIBARY IMPORT               ##
###############################################
from state_machine import (
    state_machine, start, controller, forward,
    back, left, right, turn
)
from controller import line_follower, play_music
from sokoban_solver.solver import Problem

###############################################
##              Main function                ##
###############################################
def main():

    problem = Problem("START", "SOKOBAN GAME SOLVED")
    
    task_sequence = "SFFLR"

    # STATE MACHINE
    m = state_machine()
    m.add_state("start", start)
    m.add_state("controller", controller)
    m.add_state("follow", line_follower.follow)
    m.add_state("forward", forward)
    m.add_state("left", left)
    m.add_state("right", right)
    m.add_state("turn", turn)
    m.add_state("back", back)
    m.add_state("End", None, end_state=1)
    m.set_start("start")
    m.run(task_sequence)

if __name__ == "__main__":
    main()
