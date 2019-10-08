from array import array
from collections import deque
from sokoban_games import game1, game2, game3

data = []
nrows = 0
px = py = 0
sdata = ""
ddata = ""
 
def init(board):
    global data, nrows, sdata, ddata, px, py
    # data = filter(None, board.splitlines())
    [data.append(line) for line in board.splitlines()]
    nrows = max(len(r) for r in data)
 
    maps = {' ':' ', '.': '.', '@':' ', '#':'#', '$':' '}
    mapd = {' ':' ', '.': ' ', '@':'@', '#':' ', '$':'*'}
 
    for r, row in enumerate(data):
        for c, ch in enumerate(row):
            sdata += maps[ch]
            ddata += mapd[ch]
            if ch == '@':
                px = c
                py = r
 
def push(x, y, dx, dy, data):
    if sdata[(y+2*dy) * nrows + x+2*dx] == '#' or data[(y+2*dy) * nrows + x+2*dx] != ' ':
        return None
 
    data2 = list(data)
    data2[y * nrows + x] = ' '
    data2[(y+dy) * nrows + x+dx] = '@'
    data2[(y+2*dy) * nrows + x+2*dx] = '*'
    result = ""
    for char in data2:
        result += char
    return result
 
def is_solved(data):
    for i in range(len(data)):
        if (sdata[i] == '.') != (data[i] == '*'):
            return False
    return True
 
def solve():
    open = deque([(ddata, "", px, py)])
    visited = set([ddata])
    dirs = ((0, -1, 'u', 'U'), ( 1, 0, 'r', 'R'),
            (0,  1, 'd', 'D'), (-1, 0, 'l', 'L'))
 
    lnrows = nrows
    while open:
        cur, csol, x, y = open.popleft()
 
        for di in dirs:
            temp = cur
            dx, dy = di[0], di[1]
            pos = (y+dy) * lnrows + x+dx
            if temp[pos] == '*':
                temp = push(x, y, dx, dy, temp)
                if temp and temp not in visited:
                    if is_solved(temp):
                        return csol + di[3]
                    open.append((temp, csol + di[3], x+dx, y+dy))
                    visited.add(temp)
            else:
                pos = (y+dy) * lnrows + x+dx
                if sdata[pos] == '#' or temp[pos] != ' ':
                        continue
 
                data2 = list(temp)
                past_pos = y * lnrows + x
                data2[past_pos] = ' '
                data2[pos] = '@'
                temp = ""
                for char in data2:
                    temp += char

                if temp not in visited:
                    if is_solved(temp):
                        seq = csol + di[2]
                        return seq
                    open.append((temp, csol + di[2], x+dx, y+dy))
                    visited.add(temp)
 
    return "No solution"

print("\nFirst game =>\n")
init(game1)
print(game1)
seq = solve()
print(seq)

data = []
nrows = 0
px = py = 0
sdata = ""
ddata = ""

print("\nSecond game =>\n")
init(game2)
print(game2)
seq = solve()
print(seq)

data = []
nrows = 0
px = py = 0
sdata = ""
ddata = ""

print("\nThird game =>\n")
init(game3)
print(game3)
seq = solve()
print(seq)