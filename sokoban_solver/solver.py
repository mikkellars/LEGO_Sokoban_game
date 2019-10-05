""" Module for solving  a sokoban puzzle """

# ______________________________________________________________________________
# imports
from utils import (
    is_in,
    memoize,
    PriorityQueue,
)
from sokoban_games import game3

# ______________________________________________________________________________
# Sokoban Game Solver

class Problem(object):
    """The abstract class for a formal problem."""

    def __init__(self, initial, goal=None):
        """Creates a problem class which specifies the initial state, and possibly
        a goal state, if there is a unique goal"""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Returns the actions which can be executed in the give state."""
        raise NotImplementedError

    def result(self, state, action):
        """Returns the state when the action in the state has been executed. The
        action must be one of self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Returns True if the state is a goal."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Returns the cost of a solution path that arrives at state2 from state1 with
        action, assuming cost c to get up to state1."""
        return c + 1
    
    def value(self, state):
        """For optimization problems, each state has a value. Hill-climbing and
        related algorithms try to maximize this value."""
        raise NotImplementedError

class Node:
    """ A node in a search tree contains a pointer to the parent and to the acutal 
    state for this node. Includes the action that got us to this state and the total
    path cost(g) to reach the node."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Creates a search tree node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent is not None:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step form this node."""
        return [self.child_node(problem, action) for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Returns the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]
    
    def path(self):
        """Returns a list of nodes forming the path form the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)

def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n) + h(n)."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def init(board):
    # global data, nrows, sdata, ddata, px, py
    data = filter(None, board.splitlines())
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

init(game3)