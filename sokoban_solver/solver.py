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
from sokoban_games import game1, game4 
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
    
    """
    Returns a new state based on the action and the current state
        actions can be "up", "down", "right" and "left"
    """
    def action(self, action):
        # get player position
        (row, col) = self.state.get_player_position()

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
        if char == '.' or char == 'G':
            new_state = State(pos, box_positions=None, previous_state=self.state)
            return new_state
        # check if char is a box
        elif char == 'J':
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
                return new_state

        # no valid action avaliable
        return None
    
    """ Returns the box index of box at the given position """
    def get_box_index(self, state, pos):
        # check if a box is at the given position
        positions = state.get_box_positions()
        if positions == None:
            return self.get_box_index(state.previous_state, pos)
        else:
            if isinstance(positions, list):
                for (row, col, idx) in positions:
                    if row == pos[0] and col == pos[1]:
                        return idx
            else:
                row, col, idx = positions
                if row == pos[0] and col == pos[1]:
                    return idx
        
        # stopping criteria
        if self.state.previous_state == None:
            return None

        # check previous state
        return self.get_box_index(state.previous_state, pos)


    """ Find the position of the box with the given index """
    def get_box_from_index(self, state, index):
        boxes = state.get_box_positions()
        if boxes == None:
            return self.get_box_from_index(state.previous_state, index)
        else:
            if isinstance(boxes, list):
                for row, col, idx in boxes:
                    if index == idx:
                        return row, col, idx
            else:
                row, col, idx = boxes
                if index == idx:
                    return row, col, idx
        
        if self.state.previous_state == None:
            return None

        return self.get_box_from_index(state.previous_state, index)

    """ Checks if the sokoban game is solved """
    def __is_solved__(self, state):
        boxes = []
        for i in range(self.nboxes):
            row, col, idx = self.get_box_from_index(state, i)
            boxes.append((row, col))
        
        goals = self.goal_points
        for goal in goals:
            for box in boxes:
                if goal == box:
                    boxes.remove(box)
                    goals.remove(goal)

        if len(goals) == 0 and len(boxes) == 0:
            return True
        
        return False

    """ Breadth first strategy """
    def breadth_first_strategy(self):
        # generate lists
        open_list = [] # list with unexplored states
        closed_list = [] # list with explored states (maybe not nessecary)
        actions = ["up", "down", "right", "left"]

        # start with initial state
        open_list.append(self.state)
        
        # 
        while (len(open_list) > 0):
            # pop the first element in open list
            state = open_list.pop()
            closed_list.append(state)
            self.state = state

            # if head is a goal => succes
            if self.__is_solved__(state) == True:
                return "Found the solution to this puzzle"
            else:
                for action in actions:
                    new_state = self.action(action)

                    if new_state != None:
                        open_list.append(new_state)

        return "No solutions found"

    
""" main """
solver = SokobanSolver(game1)
solver.print_board()
print(solver.breadth_first_strategy())
