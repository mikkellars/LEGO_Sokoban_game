""""""

# IMPORTS
import sys
import time
from collections import deque
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
        data = list()
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
        """Breadth first strategy
            Search the shallowest nodes in the search tree first.
            Search through tge successors of a problem to find a goal."""
        print("\nRunning breadth first search...\n")
        open = deque([(player_map, "", px, py)])
        visited = set([player_map])
        actions = (
            (0,     -1, 'u',    'U'),   # up
            (1,     0,  'r',    'R'),   # right
            (0,     1,  'd',    'D'),   # down
            (-1,    0,  'l',    'L')    # left
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
                    if data and str(data) not in visited:
                        if self.is_solved(data):
                            print("States visited: ", len(visited))
                            return seq + action[2]
                        open.append((data, seq + action[2], x+dx, y+dy))
                        visited.add(data)     
                        
def sequence2behaviors(sequence):
    """Converts the sequence to the build behaviors"""

    result = ""
    for i in range(len(sequence)):
        # get the characters
        current_char = sequence[i]
        # next_char = sequence[i+1]
        if (i != 0):
            prev_char = sequence[i-1]
        else:
            prev_char = ''

        if current_char.islower():
            if prev_char.isupper():
                result += 'T'
                result += current_char
            else:
                result += current_char
        elif current_char.isupper():
            if prev_char.islower():
                result += current_char.lower()
                result += current_char.lower()
            elif prev_char.isupper():
                if prev_char == current_char:
                    result += current_char.lower()
                else:
                    result += 'T'
                    result += current_char.lower()
                    result += current_char.lower()
            else:
                result += current_char.lower()
                result += current_char.lower()
    return result

def compass(sequence):
    """Keeps track of the robot position on the map"""

    temp_seq = list(sequence)
    result = ""
    circular_queue = deque(['u', 'r', 'd', 'l'], maxlen=4)
    char2idx = {'u':0, 'r':1, 'd':2, 'l':3}
    for i in range(len(temp_seq)):
        # get chars
        current_char = temp_seq[i]
        if i != 0:
            prev_char = temp_seq[i-1]
        else:
            prev_char = ''

        # insert char
        result += current_char

        # if chars are equal no rotation needed
        if prev_char == current_char:
            continue

        # update compass
        if current_char == 'r':
            circular_queue.rotate(1)
        elif current_char == 'l':
            circular_queue.rotate(-1)
        elif current_char == 'd':
            circular_queue.rotate(-2)
        elif current_char == 'T': 
            circular_queue.rotate(-2)
        
        # update temp_seq
        for j, char in enumerate(sequence):
            if char == 'T':
                continue
            idx = char2idx[char]
            new_char = circular_queue[idx]
            temp_seq[j] = new_char
        
    return result


""" main """
print("\n Program started\n")

solver = Solver(sokoban_games.easy)
print("Board:")
print(solver.board)
print("Number of rows:", solver.nrows)
t1 = time.time()
solution = solver.breadth_first_search()
t2 = time.time()
print("Solutions sequence:", solution)
print("Time to generate solution:", t2-t1, "seconds")

solution = sequence2behaviors(solution)
print("Sequence to behaviours:", solution)

solution = compass(solution)
print("Compass:", solution)

txtFile = open("../simple_fast/sequence.txt", 'w')
txtFile.write(solution)
txtFile.close()

print("\n Program ended\n")