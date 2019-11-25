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
import sys
import sokoban_games 
import numpy as np
import time
from collections import deque

class State:
    """ Class for storing a state """
    def __init__(self, player_position, action=None, box_positions=None, previous_state=None):
        """ constructs the class """
        # previous state
        self.previous_state = previous_state
        # list of box positions (row, col, idx)
        self.box_positions = box_positions
        self.player_position = player_position
        self.action = action

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
    
    def action(self, action):
        """
        Returns a new state based on the action and the current state
            actions can be "up", "down", "right" and "left"
        """
        # get player position
        row, col = self.state.player_position

        # get next action position
        if action == "up":
            pos = (row-1, col)
            pos2 = (row-2, col)
        elif action == "down":
            pos = (row+1, col)
            pos2 = (row+2, col)
        elif action == "right":
            pos = (row, col+1)
            pos2 = (row, col+2)
        elif action == "left":
            pos = (row, col-1)
            pos2 = (row, col-2)

        # get char at new position
        char = self.data[pos]

        # check if char free space or goal
        if char == '.' or char == 'G' or char == 'M':
            new_state = State(pos, box_positions=None, previous_state=self.state)
            return new_state
        # check if char is a box
        elif char == 'J':
            # check if move is in dead zone
            for dead_pos in self.dead_zones:
               if pos2 == dead_pos:
                   return None

            # check if box can be pushed
            char2 = self.data[pos2]
            if char2 == '.' or char2 == 'G' or char == 'M':
                idx = self.get_box_from_position(self.state, pos)
                pos2 = (pos2[0], pos2[1], idx)
                new_state = State(pos, box_positions=pos2, previous_state=self.state)
                return new_state

        # no valid action avaliable
        return None

    def get_box_from_position(self, state, pos):
        """ Returns the box index of box at the given position """

        state = self.state
        while (state != None):
            positions = state.box_positions
            if positions != None:
                if isinstance(positions, list):
                    for (row, col, idx) in positions:
                        if row == pos[0] and col == pos[1]:
                            return idx
                else:
                    row, col, idx = positions
                    if row == pos[0] and col == pos[1]:
                        return idx
            state = state.previous_state
        return None


    def get_box_from_index(self, index):
        """ Find the position of the box with the given index """
        state = self.state
        while (state != None):
            boxes = state.box_positions
            if boxes != None:
                if isinstance(boxes, list):
                    for row, col, idx in boxes:
                        if index == idx:
                            return row, col, idx
                else:
                    row, col, idx = boxes
                    if index == idx:
                        return row, col, idx
            state = state.previous_state
        return None

    def __is_solved__(self, state):
        """ Checks if the sokoban game is solved """
        goals = self.goal_points
        for goal in goals:
            row, col = goal
            if self.data[row, col] != 'J':
                return False
        return True

    def update_map(self):
        """  """
        boxes = []
        for i in range(self.nboxes):
            position = self.get_box_from_index(i)
            if position != None:
                row, col, idx = position
                boxes.append((row, col))

        # remove old boxes
        self.data = np.where(self.data == 'J', '.', self.data)

        # set new boxes
        if isinstance(boxes, list):
            for box in boxes:
                row, col = box
                self.data[row, col] = 'J'
        else:
            row, col = boxes
            self.data[row, col] = 'J'
        
        # remove old player
        self.data = np.where(self.data == 'M', '.', self.data)

        # set new player
        row, col = self.state.player_position
        if self.data[row, col] != 'G':
            self.data[row, col] = 'M'

        # insert remove goals
        for goal in self.goal_points:
            row, col = goal
            if self.data[row, col] == '.':
                self.data[row, col] = 'G'

    def create_solution_seq(self):
        """ Creates the solution sequence by looking at previous player position until initial state is reached"""
        seq = ""
        state = self.state

        # iterate back to initial state
        while (state.previous_state != None):
            # get positions
            current_pos = state.player_position
            previous_pos = state.previous_state.player_position

            # get action
            if (current_pos[0] < previous_pos[0]):
                seq += 'u'
            elif(current_pos[0] > previous_pos[0]):
                seq += 'd'
            elif(current_pos[1] < previous_pos[1]):
                seq += 'l'
            elif(current_pos[1] > previous_pos[1]):
                seq += 'r'
            
            # move on to previous state
            state = state.previous_state
        
        # flip sequence and return it
        return seq[::-1]

    def get_state_info(self, state):
        """"""
        result = []
        row, col = state.player_position
        result.append(row)
        result.append(col)
        for i in range(self.nboxes):
            row, col, idx = self.get_box_from_index(i)
            result.append(row)
            result.append(col)
            result.append(idx)
        return tuple(result)

    def breadth_first_strategy(self):
        """Breadth first strategy
            Search the shallowest nodes in the search tree first.
            Search through tge successors of a problem to find a goal."""
        print("\nRunning breadth first search algorithm..\n")

        # generate lists
        open_que = deque()
        closed = set()
        actions = ["up", "down", "right", "left"]

        # start with initial state
        open_que.append(self.state)
        
        # 
        i = 0
        while open:
            # pop the first element in open list
            state = open_que.popleft()
            self.state = state

            # store the box positions and player position and add to closed list
            state_info = self.get_state_info(state)
            closed.add(state_info)

            # Update boxes locations on the map
            self.update_map()

            # if head is a goal => succes
            if self.__is_solved__(state) == True:
                print("States visited: ", len(closed))
                return self.create_solution_seq()
            
            # keep searching
            for action in actions:
                new_state = self.action(action)
                if new_state != None:
                    new_state_info = self.get_state_info(new_state)
                    if new_state_info not in closed and new_state not in open_que:
                        open_que.append(new_state)
            
            if i % 100000 == 0:
                print("States visited: ", len(closed))
                i = 0
            i += 1

        return "No solutions found"

    def depth_first_strategy(self):
        """ Depth first strategy """
        print("\nRunning depth first search algorithm..\n")

        # generate lists
        open_list = [] # set(unordered hashtable) with unexplored states
        closed_set = set() # set with explored states (maybe not nessecary)
        actions = ["up", "down", "right", "left"]

        # start with initial state
        open_list.append(self.state)
        
        #
        while (len(open_list) > 0):
            # pop the first element in open list
            state = open_list.pop(0)
            closed_set.add(state)
            self.state = state

            # Update boxes locations on the map
            self.update_map()

            # if head is a goal => succes
            if self.__is_solved__(state) == True:
                return self.create_solution_seq()
            
            # keep searching
            for action in actions:
                new_state = self.action(action)
                if new_state != None and new_state not in closed_set:
                    open_list.insert(0, new_state)

        return "No solutions found"
    
    def a_star(self):
        """ a star search algorithm """
        print("Not implemented")
        return 0

    
""" main """
print("\nProgram started\n")
solver = SokobanSolver(sokoban_games.game2)
print("The initial board:")
print(solver.board)
print("Goal positions: ", solver.goal_points)
print("Box positions: ", solver.state.box_positions)
t1 = time.time()
seq = solver.breadth_first_strategy()
t2 = time.time()
print("Solution: ", seq)
print("Time: ", t2 - t1, " [s]")
print("\nProgram ended\n")
