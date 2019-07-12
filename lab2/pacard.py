"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import copy
from logic import *
from logicAgents import *


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


def miniWumpusSearch(problem):
    """
    A sample pass through the miniWumpus layout. Your solution will not contain 
    just three steps! Optimality is not the concern here.
    """
    from game import Directions
    e = Directions.EAST
    n = Directions.NORTH
    return [e, n, n]


def logicBasedSearch(problem):
    # # array in order to keep the ordering
    visitedStates = []
    startState = problem.getStartState()
    visitedStates.append(startState)  # Delete
    clauses = set()  ##all empiric clauses
    toVisit = util.PriorityQueue()
    toVisit.push(startState, stateWeight(startState))
    closed = set()
    uncharted = util.PriorityQueue()

    while True:
        if toVisit.isEmpty():
            if uncharted.isEmpty():
                print "I think I'll stay right here"
                return problem.reconstructPath(visitedStates)
            else:
                toVisit.push(uncharted.pop(), 0)

        position = toVisit.pop()
        if position in closed:
            continue
        visitedStates.append(position)
        closed.add(position)

        # print 'position: %d,%d' % position
        # copi = copy.deepcopy(toVisit)
        # while not copi.isEmpty():
        #     print copi.pop()

        if problem.isGoalState(position):
            print 'Game over: Teleported home!'
            return problem.reconstructPath(visitedStates)

        stench = problem.isWumpusClose(position)
        breeze = problem.isPoisonCapsuleClose(position)
        glow = problem.isTeleporterClose(position)

        # mark current safe (should always happen)
        if not stench and not breeze:
            clauses.add(Clause(returnSet(Literal('o', position))))
            # mark surrounding states safe (only if no stench or smth)
            safeRule(problem.getSuccessors(position), clauses)

        ##these three cover first six rules
        makeStatements(problem, position, stench, 'w', clauses)
        makeStatements(problem, position, breeze, 'p', clauses)
        makeStatements(problem, position, glow, 't', clauses)

        for succ in problem.getSuccessors(position):
            if succ[0] in closed:
                continue
            w = checkClosure(succ[0], 'w', clauses)
            if w:
                continue
            p = checkClosure(succ[0], 'p', clauses)
            if p:
                continue
            t = checkClosure(succ[0], 't', clauses)
            if t:
                toVisit.push(succ[0], 0)  # TOP priority
                # continue
            # ADD WPO RULE
            s = set()
            s.add(Literal('w', succ[0]))
            s.add(Literal('p', succ[0]))
            s.add(Literal('o', succ[0]))
            clauses.add(Clause(s))

            # CHECK safe successors, add toVisit
            if resolution(clauses, Clause(returnSet(Literal('o', succ[0])))):
                toVisit.push(succ[0], stateWeight(succ[0]))
                pushed = True
                continue
            if stench or breeze:
                heur = 200
            if glow:
                heur = -20
            uncharted.push(succ[0], stateWeight(succ[0]) + heur)


def checkClosure(succ, char, clauses):
    return resolution(clauses, Clause(returnSet(Literal(char, succ))))


def returnSet(lit):
    s = set()
    s.add(lit)
    return s


def safeRule(succs, clauses):
    for succ in succs:
        clauses.add(Clause(returnSet(Literal('o', succ[0]))))


def makeStatements(problem, position, isclose, char, clauses):
    if isclose:
        orLiterals = set()  ##for the big clause
        for succ in problem.getSuccessors(position):
            orLiterals.add(Literal(char, succ[0]))  ##LABEL, STATE, NEGATIVE
        clauses.add(Clause(orLiterals))  # the big disjunct clause
        # we are sure one of these is true
    else:
        for succ in problem.getSuccessors(position):
            clauses.add(Clause(returnSet(Literal(char, succ[0], True))))  # '4' small conjuct clauses
            # we are sure these all are true


# Abbreviations
lbs = logicBasedSearch
