""" Module for solving  a sokoban puzzle

    'X' is a wall
    '.' is a free space
    'J' is start position of a box
    'G' is a goal place
    'M' it start position of the sokoban worker


    '*' is a box placed on a goal
    '+' is for sokoban worker on a goal

    "flrb" are the moves and uppercase, "FLRB" for pushes.
"""

""" IMPORTS """
import os
import sys
import sokoban_games 
import numpy as np
import time
from collections import deque # list-like container with fast appends and pops on either end
import copy
import psutil

class State:
    """ Class for storing a state """
    def __init__(self, player_position, box_positions=None, previous_state=None, action=None):
        """ constructs the class """
        self.previous_state = previous_state
        self.box_positions = box_positions
        self.player_position = player_position
        self.action = action

    def get_previous_state(self):
        return copy.deepcopy(self.previous_state)

    def get_box_position(self):
        return copy.deepcopy(self.box_positions)

    def get_player_position(self):
        return copy.deepcopy(self.player_position)
    
    def get_action(self):
        return copy.deepcopy(self.action)

class SokobanSolver:
    """ Class for solving a sokoban board """
    def __init__(self, board):
        """ construct the class """
        # store initial board
        self.board = board

        # generate board as data
        self.__board2matrix__() # as matrix
        #self.__board2strings__() # as list of strings

        # get list of dead zones
        self.__dead_zones__()

    def print_board(self):
        """ Prints the board in its inital state """
        print("The current board:")
        print(self.board)
    
    def __board2matrix__(self):
        """ Generates a matrix of the board"""
        # get lines
        lines = []
        [lines.append(line) for line in self.board.splitlines()]

        # get width and height of the borad
        cols = max(len(line) for line in lines)
        rows = len(lines)

        # generate board with nothing
        matrix = [[0 for x in range(cols)] for y in range(rows)]

        # fill in board
        goal_points = []
        box_positions = []
        idx = 0
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                matrix[row][col] = char
                if char == 'M':
                    player_position = (row, col)
                if char == 'G':
                    goal_points.append((row, col))
                if char == 'J':
                    box_positions.append((row, col, idx))
                    idx += 1

        # create initial state
        inital_state = State(player_position, box_positions)

        # convert to numpy array
        matrix = np.asarray(matrix)

        # store generated data
        self.state = inital_state
        self.goal_points = goal_points
        self.data = matrix
        self.ncols = cols
        self.nboxes = len(box_positions)
    
    # """ Generate board as list of strings """
    # def __board2strings__(self):
    #     # store lines in data
    #     lines = []
    #     [lines.append(line) for line in self.board.splitlines()]

    #     # get number of rows
    #     cols = max(len(r) for r in lines)

    #     # get start point and goal points
    #     goal_points = []
    #     box_positions = []
    #     for i, row in enumerate(lines):
    #         for j, char in enumerate(row):
    #             if char == 'M':
    #                 player_position = (i, j)
    #             if char == 'G':
    #                 goal_points.append((i, j))
    #             if char == 'J':
    #                 box_positions.append((i, j))

    #     # create initial state
    #     state = State(box_positions, player_position)
        
    #     # store generate data
    #     self.inital_state = state
    #     self.goal_points = goal_points
    #     self.data = lines
    #     self.nrows = cols

    def __dead_zones__(self):
        """ Checks for dead zones in the map, where the box cannot be push to and stores them """
        self.dead_zones = self.__check_corners__()
        
    def __check_corners__(self):
        """ Finds unnessesary corners """
        # create corners
        filter_up_left = np.array([['X','X'],['X','.']])
        filter_up_left_man = np.array([['X','X'],['X','M']])
        filter_up_right = np.array([['X','X'],['.','X']])
        filter_up_right_man = np.array([['X','X'],['M','X']])
        filter_down_left = np.array([['X','.'],['X','X']])
        filter_down_left_man = np.array([['X','M'],['X','X']])
        filter_down_right = np.array([['.','X'],['X','X']])
        filter_down_right_man = np.array([['M','X'],['X','X']])

        # get dead zones
        dead_zones = []
        for row in range(np.size(self.data, 0) - 1): # rows checking
            for col in range(np.size(self.data, 1) - 1): 
                if ((self.data[row:row+2, col:col+2] == filter_down_left).all()) or ((self.data[row:row+2, col:col+2] == filter_down_left_man).all()):
                    dead_zones.append((row, col+1))
                elif ((self.data[row:row+2, col:col+2] == filter_up_left).all()) or ((self.data[row:row+2, col:col+2] == filter_up_left_man).all()):
                    dead_zones.append((row+1, col+1))
                elif ((self.data[row:row+2, col:col+2] == filter_down_right).all()) or ((self.data[row:row+2, col:col+2] == filter_down_right_man).all()):
                    dead_zones.append((row, col))
                elif ((self.data[row:row+2, col:col+2] == filter_up_right).all()) or ((self.data[row:row+2, col:col+2] == filter_up_right_man).all()):
                    dead_zones.append((row+1, col))

        return dead_zones
    
    def action(self, action, state, map):
        """
        Returns a new state based on the action and the current state
            actions can be "up", "down", "right" and "left"
        """
        # get player position
        row, col = state.player_position

        # get next action position
        if action == "u":
            pos = (row-1, col)
            pos2 = (row-2, col)
        elif action == "d":
            pos = (row+1, col)
            pos2 = (row+2, col)
        elif action == "r":
            pos = (row, col+1)
            pos2 = (row, col+2)
        elif action == "l":
            pos = (row, col-1)
            pos2 = (row, col-2)
        # get char at new position
        char = map[pos]

        # check if char free space or goal
        if char == '.' or char == 'G' or char == 'M':
            new_state = State(pos, box_positions=state.get_box_position(), previous_state=state, action=action)
            return new_state
        # check if char is a box
        elif char == 'J':
            # check if move is in dead zone
            for dead_pos in self.dead_zones:
               if pos2 == dead_pos:
                   return None

            # check if box can be pushed
            char2 = map[pos2]
            if char2 == '.' or char2 == 'G':
                idx = self.get_box_from_position(state, pos)
                pos2 = (pos2[0], pos2[1], idx)
                # Update the box that is moved
                boxes = state.get_box_position()
                boxes[idx] = pos2
                new_state = State(pos, box_positions=boxes, previous_state=state, action=action)
                return new_state
        # no valid action avaliable
        return None

    def get_box_from_position(self, state, pos):
        """ Returns the box index of box at the given position """
        boxes = state.get_box_position()
        for (row, col, idx) in boxes:
            if row == pos[0] and col == pos[1]:
                return idx

    def __is_solved__(self, state, map):
        """ Checks if the sokoban game is solved """
        goals = self.goal_points
        for goal in goals:
            row, col = goal
            if map[row, col] != 'J':
                return False
        return True

    def update_map(self, state, map):
        """  """
        boxes = state.get_box_position()
        player = state.get_player_position()

        # remove old boxes and player
        map = np.where(map == 'J', '.', map)
        map = np.where(map == 'M', '.', map)

        # set new player
        for goal in self.goal_points:
            if goal != player:
                map[player] = 'M'
        
        # insert boxes
        for box in boxes:
            map[box[0], box[1]] = 'J'

        # insert goals
        for goal in self.goal_points:
            if map[goal] != 'J':
                map[goal] = 'G'

        return map

    def create_solution_seq(self, state):
        """ Creates the solution sequence by looking at previous player position until initial state is reached"""
        seq = ""
        while (state.get_previous_state() != None):
            # get positions
            seq += state.get_action()
            state = state.get_previous_state()

        # flip sequence and return it
        return seq[::-1]

        # seq = ""
        # state = self.state

        # # iterate back to initial state
        # while (state.previous_state != None):
        #     # get positions
        #     current_pos = state.get_player_position()
        #     previous_pos = state.get_previous_state().get_player_position()

        #     # get action
        #     if (current_pos[0] < previous_pos[0]):
        #         seq += 'u'
        #     elif(current_pos[0] > previous_pos[0]):
        #         seq += 'd'
        #     elif(current_pos[1] < previous_pos[1]):
        #         seq += 'l'
        #     elif(current_pos[1] > previous_pos[1]):
        #         seq += 'r'
            
        #     # move on to previous state
        #     state = state.get_previous_state()
        
        # # flip sequence and return it
        # return seq[::-1]

    def get_state_info(self, state):
        """Return the state info (player position and box positions) as one tuple"""
        result = []
        action = state.get_action()
        result.append(action)
        row, col = state.get_player_position()
        result.append(row)
        result.append(col)
        boxes = state.get_box_position()
        for box in boxes:
            row, col, idx = box
            result.append(row)
            result.append(col)
            result.append(idx)
        return tuple(result)

    def breadth_first_strategy(self):
        """Breadth first strategy
            Search the shallowest nodes in the search tree first.
            Search through tge successors of a problem to find a goal."""
        
        print("\nRunning breadth first search algorithm..\n")

        # get time
        t1 = time.time()

        # generate lists
        open_queue = deque()
        closed_set = set() # set with explored states (maybe not nessecary)
        actions = ["u", "d", "r", "l"]

        # start with initial state
        current_map = self.data
        open_queue.append(self.state)

        # i = 0
        while open_queue:
            # pop the first element in open list
            current_state = open_queue.popleft()

            # store the box positions and player position and add to closed list
            state_info = self.get_state_info(current_state)
            closed_set.add(state_info)
            
            # Update boxes locations on the map
            current_map = self.update_map(current_state, current_map)
            
            # if head is a goal => succes
            if self.__is_solved__(current_state, current_map) == True:
                print("States visited: ", len(closed_set))
                return self.create_solution_seq(current_state)
            
            # keep searching
            for action in actions:
                new_state = self.action(action, current_state, current_map)
                if new_state != None:
                    new_state_info = self.get_state_info(new_state)
                    if new_state_info not in closed_set:
                        open_queue.append(new_state)
            
            # if i % 100000 == 0:
            #     print("States visited: ", len(closed_set))
            #     #print(current_state.get_action())
            #     print(current_map)
            #     i = 0
            # i += 1

            # check if 15 min has passed
            t2 = time.time()
            if (t2 - t1) > 900:
                print("Time exceeded 15 min")
                return "No sulotions found"

        return "No solutions found"

    # def depth_first_strategy(self):
    #     """ Depth first strategy """
    #     print("\nRunning depth first search algorithm..\n")

    #     # generate lists
    #     open_list = [] # set(unordered hashtable) with unexplored states
    #     closed_set = set() # set with explored states (maybe not nessecary)
    #     actions = ["up", "down", "right", "left"]

    #     i = 0

    #     # start with initial state
    #     open_list.append(self.state)
        
    #     #
    #     while (len(open_list) > 0):
    #         # pop the first element in open list
    #         self.state = open_list.pop(0)
    #         # store the box positions and player position and add to closed list
    #         state_info = self.get_state_info(self.state)
    #         closed_set.add(state_info)

    #         # Update boxes locations on the map
    #         self.update_map()

    #         # if head is a goal => succes
    #         if self.__is_solved__(self.state) == True:
    #             return self.create_solution_seq()
            
    #         # keep searching
    #         for action in actions:
    #             new_state = self.action(action)
    #             if new_state != None:
    #                 new_state_info = self.get_state_info(new_state)
    #                 if new_state_info not in closed_set:
    #                      open_list.insert(0, new_state)

    #         if i % 1 == 0:
    #             print("States visited: ", len(closed_set))
    #             print(self.data)
    #             #i = 0
    #         i += 1

    #     return "No solutions found"
    
    def a_star(self):
        """ a star search algorithm """
        print("Not implemented")
        return 0

    
""" main """

print("\nProgram started\n")

# get games
games = list()
games.append(sokoban_games.game1)
games.append(sokoban_games.game2)
games.append(sokoban_games.game3)
games.append(sokoban_games.game4)
games.append(sokoban_games.game5)

# solve all games
times = list()
memories = list
for game in games:
    solver = SokobanSolver(game)
    
    print("The initial board:")
    print(solver.board)
    
    print("Goal positions: ", solver.goal_points)
    print("Box positions: ", solver.state.box_positions)
    
    t1 = time.time()
    seq = solver.breadth_first_strategy()
    t2 = time.time()

    print("Solution: ", seq)
    print("Time: ", t2 - t1, " [s]")

    pid = os.getpid()
    process = psutil.Process(pid)
    print("Memory usage:", process.memory_info()[0])

    times.append((t2-t1))
    memories.append(process.memory_info()[0])

for time in times:
    print(time)

print("\nProgram ended\n")
