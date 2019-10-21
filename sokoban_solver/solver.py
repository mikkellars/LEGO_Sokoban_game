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
from sokoban_games import game4 
import numpy as np

""" Class for storing a state """
class State:
    """ constructs the class """
    def __init__(self, player_position, box_positions=None, previous_state=None):
        # previous state
        self.previous_state = previous_state
        
        # list of box positions (row, col, idx)
        self.box_positions = box_positions
        self.player_position = player_position

    """ returns previous state """
    def get_previours_state(self):
        return self.previous_state

    """ returns the change box and its positions """
    def get_box_positions(self):
        return self.box_positions
    
    """ returns player position """
    def get_player_position(self):
        return self.player_position

""" Class for solving a sokoban board """
class SokobanSolver:
    """ construct the class """
    def __init__(self, board):
        # store initial board
        self.board = board

        # generate board as data
        self.__board2matrix__() # as matrix
        #self.__board2strings__() # as list of strings

        # get list of dead zones
        self.__dead_zones__()

    """ Prints the board in its inital state """
    def print_board(self):
        print("The current board =>\n")
        print(self.board)
        print("\n")
    
    """ Print dead zones """

    
    """ Generates a matrix of the board"""
    def __board2matrix__(self):
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

    """ Checks for dead zones in the map, where the box cannot be push to,
        and stores them """
    def __dead_zones__(self):
        self.dead_zones = self.__check_corners__()
        
    """ Finds unnessesary corners """
    def __check_corners__(self):
        # create corners
        filter_up_left = np.array([['X','X'],['X','.']])
        filter_up_right = np.array([['X','X'],['.','X']])
        filter_down_left = np.array([['X','.'],['X','X']])
        filter_down_right = np.array([['.','X'],['X','X']])

        # get dead zones
        dead_zones = []
        for row in range(np.size(self.data, 0) - 1): # rows checking
            for col in range(np.size(self.data, 1) - 1): 
                if((self.data[row:row+2, col:col+2] == filter_down_left).all()):
                    dead_zones.append((row, col+1))
                elif((self.data[row:row+2, col:col+2] == filter_up_left).all()):
                    dead_zones.append((row+1, col+1))
                elif((self.data[row:row+2, col:col+2] == filter_down_right).all()):
                    dead_zones.append((row, col))
                elif((self.data[row:row+2, col:col+2] == filter_up_right).all()):
                    dead_zones.append((row+1, col))

        return dead_zones
    
    """ Return a new state based on the given action """
    def action(self, action):
        if action == "up":
            # get player position
            (row, col) = self.state.get_player_position()
            
            # get char at new position
            pos = (row-1, col)
            char = self.data[pos]

            # check if char free space or goal
            if char == '.' or char == 'G':
                new_state = State(pos, box_positions=None, previous_state=self.state)
                self.state = new_state
            # check if char is a box
            elif char == 'J':
                # check if box can be moved
                pos2 = (row-2, col)

                # check if move is in dead zone
                for dead_pos in self.dead_zones:
                    if pos2 == dead_pos:
                        return None
                
                # get char at new position
                char2 = self.data[pos2]
                
                if char2 == '.' or char2 == 'G':
                    idx = self.get_box_index(self.state, pos)
                    pos2 = (pos2[0], pos2[1], idx)
                    new_state = State(pos, box_positions=pos2, previous_state=self.state)
                    self.state = new_state
        elif action == "down":
            pass
        elif action == "right":
            pass
        elif action == "left":
            pass

        # no valid action avaliable
        return None
    
    """ Returns the box index of box at the given position """
    def get_box_index(self, state, pos):
        positions = state.get_box_positions()
        for (row, col, idx) in positions:
            if row == pos(0) and col == pos(1):
                return idx
        
        self.get_box_index(state.previous_state, pos)
    
""" main """
solver = SokobanSolver(game4)
solver.print_board()