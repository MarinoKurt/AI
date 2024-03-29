# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import copy

class SearchNode:
    """
    This class represents a node in the graph which represents the search problem.
    The class is used as a basic wrapper for search methods - you may use it, however
    you can solve the assignment without it.

    REMINDER: You need to fill in the backtrack function in this class!
    """

    def __init__(self, position, parent=None, transition=None, cost=0, heuristic=0):
        """
        Basic constructor which copies the values. Remember, you can access all the 
        values of a python object simply by referencing them - there is no need for 
        a getter method. 
        """
        self.position = position
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.transition = transition

    def isRootNode(self):
        """
        Check if the node has a parent.
        returns True in case it does, False otherwise
        """
        return self.parent == None

    def unpack(self):
        """
        Return all relevant values for the current node.
        Returns position, parent node, cost, heuristic value
        """
        return self.position, self.parent, self.cost, self.heuristic

    def backtrack(self, problem):
        """
        Reconstruct a path to the initial state from the current node.
        Bear in mind that usually you will reconstruct the path from the 
        final node to the initial.
        """
        moves = []
        # make a deep copy to stop any referencing isues.
        node = copy.deepcopy(self)

        if node.isRootNode():
            # The initial state is the final state
            return moves

        "**YOUR CODE HERE**"
        # non recursive s
        # while not node.isRootNode():
        #     parent = node.parent
        #     for suc in problem.getSuccessors(parent.position):
        #         if suc[0] == node.position:
        #             moves.append(suc[1]) #action
        #     node = parent
        # moves.reverse()
        # return moves

        # recursive
        moves = self.parent.backtrack(problem)
        moves.append(self.transition)
        return moves

        # util.raiseNotDefined()


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    open = util.Stack()
    open.push(SearchNode(problem.getStartState(), None, "Stop", 0, 0))
    closed = []

    while not open.isEmpty():
        current = open.pop()
        if problem.isGoalState(current.position):
            return current.backtrack(problem)

        if current not in closed:
            closed.append(current.position)

            # child x,y,z: x is position, y action, z cost
            for child in problem.getSuccessors(current.position):
                if child[0] not in closed:
                    open.push(SearchNode(child[0], current, child[1], 0))
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    open = util.Queue()
    open.push(SearchNode(problem.getStartState(), None, "Stop", 0, 0))
    closed = []

    while not open.isEmpty():
        current = open.pop()
        if problem.isGoalState(current.position):
            return current.backtrack(problem)

        if current not in closed:
            closed.append(current.position)

            # child x,y,z: x is position, y action, z cost
            for child in problem.getSuccessors(current.position):
                if child[0] not in closed:
                    seen = False
                    for it in open.list:
                        if it.position == child[0]:
                            seen = True
                    if not seen:
                        open.push(SearchNode(child[0], current, child[1], 0))
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    open = util.PriorityQueue()
    open.push(SearchNode(problem.getStartState(), None, "Stop", 0, 0), 0)
    closed = []
    closedPositions = []

    while not open.isEmpty():
        current = open.pop()
        if problem.isGoalState(current.position):
            return current.backtrack(problem)

        if current.position not in closedPositions:
            closedPositions.append(current.position)
            closed.append(current)

            # child x,y,z: x is position, y action, z cost
            for child in problem.getSuccessors(current.position):
                if child[0] not in closedPositions:
                    open.push(SearchNode(child[0], current, child[1], child[2]+current.cost), child[2]+current.cost)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic): #default: nullHeuristic
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    open = util.PriorityQueue()
    open.push(SearchNode(problem.getStartState(), None, "Stop", 0, 0), 0)
    closed = []
    closedPositions = []

    while not open.isEmpty():
        current = open.pop()
        if problem.isGoalState(current.position):
            return current.backtrack(problem)

        if current.position not in closedPositions:
            closedPositions.append(current.position)
            closed.append(current)

            # child x,y,z: x is position, y action, z cost
            for child in problem.getSuccessors(current.position):

                if child[0] not in closedPositions:
                    sn = SearchNode(child[0], current, child[1], child[2] + current.cost, heuristic(child[0], problem))
                    open.push(sn, child[2] + current.cost+ heuristic(child[0], problem))
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
