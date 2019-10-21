# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        scoreDiff = successorGameState.getScore()
        "*** YOUR CODE HERE ***"
        # tính khoảng cách manhattan tới ma gần nhất
        newpos2ghost_distances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        closestghost = min(newpos2ghost_distances)
        foodList = newFood.asList()
        if foodList:
            newpos2food_distances = [manhattanDistance(newPos, food) for food in foodList]
            closestfood = min(newpos2food_distances)  # khoảng cách manhattan tới thức ăn gần nhất
        else:
            closestfood = 0
        score = (15 / (closestfood + 1)) + (80 / (len(foodList) + 1)) + scoreDiff
        # có sợ ma gần nhất hay không
        if newScaredTimes[newpos2ghost_distances.index(closestghost)] <= 0:
            score += (-20 / (closestghost + 1))  # giảm điểm khi càng gần với ma gần nhất
        return score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        bestMove, score = minimax_search(self, gameState, 0, 0)
        return bestMove


def minimax_search(self, gameState, agentIndex, depth):
    bestMove = None
    # kiểm tra trạng thái thắng, thua, đã duyệt dủ sâu
    if gameState.isWin() or gameState.isLose() or depth >= self.depth:
        return bestMove, self.evaluationFunction(gameState)
    score = float("Inf")
    if agentIndex == 0:  # là max agent
        score = -float("Inf")

    moves = gameState.getLegalActions(agentIndex)
    # duyệt tất cả các hướng đi
    for move in moves:
        next_gameState = gameState.generateSuccessor(agentIndex, move)
        if agentIndex == 0:  # max agent
            next_move, next_score = minimax_search(self, next_gameState, agentIndex + 1, depth)
            if next_score > score:  # chọn hướng đi cho điểm cao hơn cho max agent
                score = next_score
                bestMove = move
        else:
            if agentIndex == (gameState.getNumAgents() - 1):
                next_agent = 0
                depth_next = depth + 1
            else:
                next_agent = agentIndex + 1
                depth_next = depth
            next_move, next_score = minimax_search(self, next_gameState, next_agent, depth_next)
            if next_score < score:  # chọn hướng đi có điểm thấp hơn cho min agent
                score = next_score
                bestMove = move
    return bestMove, score


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestAction, score = alpha_beta(self, gameState, 0, 0, -float("Inf"), float("Inf"))
        return bestAction


def alpha_beta(self, gameState, agentIndex, depth, alpha, beta):
    bestMove = None
    if gameState.isWin() or gameState.isLose() or depth >= self.depth:
        return bestMove, self.evaluationFunction(gameState)
    score = float("Inf")
    if agentIndex == 0:
        score = -float("Inf")

    moves = gameState.getLegalActions(agentIndex)
    for move in moves:
        next_gameState = gameState.generateSuccessor(agentIndex, move)
        if agentIndex == 0:  # là max agent
            next_move, next_score = alpha_beta(self, next_gameState, agentIndex + 1, depth, alpha, beta)
            if next_score > score:
                score = next_score
                bestMove = move
            alpha = max(score, alpha)
            if score > beta:
                return bestMove, score
        else:
            if agentIndex == (gameState.getNumAgents() - 1):
                next_agent = 0
                depth_next = depth + 1
            else:
                next_agent = agentIndex + 1
                depth_next = depth
            next_move, next_score = alpha_beta(self, next_gameState, next_agent, depth_next, alpha, beta)
            if next_score < score:
                score = next_score
                bestMove = move
            beta = min(score, beta)
            if score < alpha:
                return bestMove, score
    return bestMove, score


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        bestAction, score = expectimax_search(self, gameState, 0, 0)
        return bestAction


def expectimax_search(self, gameState, agentIndex, depth):
    bestMove = None
    if gameState.isWin() or gameState.isLose() or depth >= self.depth:
        return bestMove, self.evaluationFunction(gameState)
    score = 0
    if agentIndex == 0:
        score = -float("Inf")

    moves = gameState.getLegalActions(agentIndex)

    for move in moves:
        next_gameState = gameState.generateSuccessor(agentIndex, move)
        if agentIndex == 0:  # là max agent
            next_move, next_score = expectimax_search(self, next_gameState, agentIndex + 1, depth)
            if next_score > score:
                score = next_score
                bestMove = move
        else:
            if agentIndex == (gameState.getNumAgents() - 1):
                next_agent = 0
                depth_next = depth + 1
            else:
                next_agent = agentIndex + 1
                depth_next = depth
            next_move, next_score = expectimax_search(self, next_gameState, next_agent, depth_next)
            score = score + (1 / float(len(moves))) * next_score
    return bestMove, score


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
