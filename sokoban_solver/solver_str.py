""""""

# IMPORTS
import sys
import time
from collections import deque
from copy import deepcopy, copy
import sokoban_games

# GLOBALS
goal_map = player_map = ""
px = py = 0

# FUNCTIONS
class Solver:
    """Solves a sokoban puzzle"""

    def __init__(self, board):
        """init function"""
        global player_map, goal_map, px, py
        self.board = board
        # collect important data
        data = []
        [data.append(line) for line in board.splitlines()]
        self.nrows = max(len(row) for row in data)
        # generate maps
        create_goal_map = {'.':'.', 'G':'G', 'M':'.', 'X':'X', 'J':'.'}
        create_player_map = {'.':'.', 'G':'.', 'M':'M', 'X':'X', 'J':'J'}
        for r, row in enumerate(data):
            for c, char in enumerate(row):
                goal_map += create_goal_map[char]
                player_map += create_player_map[char]
                if char == 'M':
                    px = c
                    py = r
    
    def push(self, x, dx, y, dy, data):
        """Push the can and update map"""
        pos = y * self.nrows + x
        pos1 = (y + dy) * self.nrows + x + dx
        pos2 = ((y + (2*dy)) * self.nrows) + x + (2*dx)
        char = data[pos2]
        if char != '.':
            return None
        new_data = list(data)
        new_data[pos] = '.'
        new_data[pos1] = 'M'
        new_data[pos2] = 'J'
        data = ""
        for char in new_data:
            data += char
        return data
    
    def is_solved(self, data):
        """Checks if the puzzle is solved"""
        for i in range(len(data)):
            if (goal_map[i] == 'G') != (data[i] == 'J'):
                return False
        return True

    def breadth_first_search(self):
        """Solves the puzzle"""
        open = deque([(player_map, "", px, py)])
        visited = set([player_map])
        actions = (
            (0, -1, 'u', 'U'),  # up
            (1, 0, 'r', 'R'),   # right
            (0, 1, 'd', 'D'),   # down
            (-1, 0, 'l', 'L')   # left
        )
        while open:
            current_map, seq, x, y = open.popleft()
            for action in actions:
                data = current_map
                dx, dy = action[0], action[1]
                pos = (y + dy) * self.nrows + (x + dx)
                char = data[pos]
                # check for box 'J'
                if char == 'J':
                    data = self.push(x, dx, y, dy, data)
                    if data and data not in visited:
                        # check if the puzzle is solved
                        if self.is_solved(data):
                            print("States visited: ", len(visited))
                            return seq + action[3]
                        open.append((data, seq + action[3], x+dx, y+dy))
                        visited.add(data)
                elif char == 'X':
                    continue
                else:
                    # move player and generate new string
                    previous_pos = y * self.nrows + x
                    new_data = list(data)
                    new_data[previous_pos] = '.'
                    new_data[pos] = 'M'
                    data = ""
                    for char in new_data:
                        data += char
                    # check if temp has been visited before
                    if data and data not in visited:
                        if self.is_solved(data):
                            print("States visited: ", len(visited))
                            return seq + action[2]
                        open.append((data, seq + action[2], x+dx, y+dy))
                        visited.add(data)          

""" main """
solver = Solver(sokoban_games.game7)
print("Board:")
print(solver.board)
print("Number of rows:", solver.nrows)

# # print goal map
# print("Goal map:")
# txt = ""
# for i, char in enumerate(goal_map):
#     txt += char
#     if (i+1) % solver.nrows == 0:
#         print(txt)
#         txt = ""

# # print player map
# print("Player map:")
# txt = ""
# for i, char in enumerate(player_map):
#     txt += char
#     if (i+1) % solver.nrows == 0:
#         print(txt)
#         txt = ""

t1 = time.time()
solution = solver.breadth_first_search()
t2 = time.time()
print("Solutions sequence:", solution)
print("Time to generate solution:", t2-t1, "seconds")