""" Module for solving  a sokoban puzzle """

# ______________________________________________________________________________
# imports
import math
import random
import sys
import functools
import heapq

# ______________________________________________________________________________
# Sokoban Game Solver

def is_valid_value(char):
    if (char == ' ' or # floor
        char == '#' or # wall
        char == '@' or # worker on floor
        char == '.' or # goal
        char == '*' or # box on goal
        char == '$' or # box
        char == '+' ): # worker on goal
        return True
    else:
        return False

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

def is_in(elt, seq):
    """Similar to (elt in seq), but compares with 'is', not '=='."""
    return any(x is elt for x in seq)

def hamming_distance(X, Y):
    return sum(x != y for x, y in zip(X, Y))

def manhattan_distance(X, Y):
    return sum(abs(x - y) for x, y in zip(X, Y))

def distance(a, b):
    """The distance between two (x, y) points."""
    xA, yA = a
    xB, yB = b
    return math.hypot((xA - xB), (yA - yB))

def distance_squared(a, b):
    """The square of the distance between two (x, y) points."""
    xA, yA = a
    xB, yB = b
    return (xA - xB) ** 2 + (yA - yB) ** 2

def memoize(fn, slot=None, maxsize=32):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, use lru_cache for caching the values."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    return memoized_fn

class PriorityQueue:
    """A Queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first.
    If order is 'min', the item with minimum f(x) is
    returned first; if order is 'max', then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order='min', f=lambda x: x):
        self.heap = []

        if order == 'min':
            self.f = f
        elif order == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
        else:
            raise ValueError("order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

    def __contains__(self, key):
        """Return True if the key is in PriorityQueue."""
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        """Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present."""
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)