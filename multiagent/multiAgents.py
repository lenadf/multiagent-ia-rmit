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
import random, util, sys

from game import Agent

# To simulate infinity and negative infinity
INF = sys.maxint
NEGATIVE_INF = -sys.maxint - 1

def minimumSpanningTree(gameState):
    """
    Return the minimum spanning tree
    Vertex are the positions with food inside AND the current positions
    Edges values are manhattanDistance between vertex
    """
    pos = gameState.getPacmanPosition()
    food = gameState.getFood()


    # Initialize Prim algorithm
    pqueue = util.PriorityQueue()
    G = set()
    cost = {}
    pred = {}

    cost[pos] = 0
    G.add(pos)

    for x in range(food.width):
        for y in range(food.height):
            if (food[x][y]):
                posFood = (x,y)
                G.add(posFood)
                cost[posFood] = INF # Infinity value
                pred[posFood] = None

    for v in G:
        pqueue.push(v, cost[v])

    # Main loop Prim
    while (not pqueue.isEmpty()):
        t = pqueue.pop()
        for u in G:
            w = util.manhattanDistance(u, t)
            if (u != t) and (cost[u] > w):
                pred[u] = t
                cost[u] = w
                pqueue.push(u, cost[u]) # Update the priority queue with the new value

    return pred


def getValueMST(pred, gameState):
    totalWeight = 0

    for u in pred:
        totalWeight += util.manhattanDistance(u, pred[u])

    return totalWeight


def getDistClosestFood(gameState):
    pos = gameState.getPacmanPosition()
    food = gameState.getFood()
    minDist = INF

    for x in range(food.width):
        for y in range(food.height):
            if food[x][y] == True:
                dist = util.manhattanDistance(pos, (x, y))

                if dist < minDist:
                    minDist = dist

    return minDist


def getDistClosestGhost(gameState):
    pos = gameState.getPacmanPosition()
    ghostStates = gameState.getGhostStates()

    distClosestUnscaredGhost = INF
    distClosestScaredGhost = NEGATIVE_INF

    for ghost in ghostStates:
        distToGhost = util.manhattanDistance(pos, ghost.getPosition())

        if (ghost.scaredTimer > distToGhost) and (distToGhost < distClosestScaredGhost):
            # We are in range, try to beat him !
            distClosestScaredGhost = distToGhost
        elif (distToGhost < distClosestUnscaredGhost):
            # Runaway
            distClosestUnscaredGhost = distToGhost

    # Because we don't want to consider those parameters if they are not representative
    distClosestUnscaredGhost = max(0, distClosestUnscaredGhost)
    distClosestScaredGhost = max(0, distClosestScaredGhost)

    return (distClosestUnscaredGhost, distClosestScaredGhost)


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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        newGhostStates = successorGameState.getGhostStates() #Tableau
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] #Tableau

        "*** YOUR CODE HERE ***"
        # We don't want to get stuck
        if (action == 'Stop'):
            return NEGATIVE_INF

        # To improve the coefficients we could have used some machine learning algorithms (genetic programming, svm, etc.)
        coefficients = {}
        coefficients['COEF_gameScore'] = 1
        coefficients['COEF_distClosestFood'] = -2
        coefficients['COEF_distClosestUnscaredGhost'] = 1.5
        coefficients['COEF_distClosestScaredGhost'] = 2000
        coefficients['COEF_foodLeft'] = -20
        coefficients['COEF_capsulesLeft'] = -50

        # betterEvaluationFunction is evaluationFunction with some features improved
        # So we prefer to call it directly to improve readability and code factorisation
        return genericEvaluationFunction(successorGameState, coefficients) - genericEvaluationFunction(currentGameState, coefficients)


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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'): #scoreEvaluationFunction
        self.index = 0 # Pacman is always agent index 0
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
        """
        "*** YOUR CODE HERE ***"
        self.numGhosts = gameState.getNumAgents() - 1
        legal = gameState.getLegalActions(0)
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        maxScore = NEGATIVE_INF
        maxAction = None

        for action in legal:
            successorGameState = gameState.generateSuccessor(0, action)
            score = self.DFSMiniMax(successorGameState, 0, 1)

            if score > maxScore:
                maxScore = score
                maxAction = action

        return action


    def DFSMiniMax(self, gameState, agentIndex, currentDepth):
        if gameState.isWin() or gameState.isLose() or currentDepth > self.depth:
            # gameState is a terminal state or has reached the maximum depth of minimax algo
            return self.evaluationFunction(gameState)

        legal = gameState.getLegalActions(agentIndex)
        if Directions.STOP in legal: legal.remove(Directions.STOP)
        successors = [(gameState.generateSuccessor(agentIndex, action), action) for action in legal]

        if agentIndex == 0: # Pacman
            return max([self.DFSMiniMax(successor[0], 1, currentDepth) for successor in successors])
        else: # Ghost
            return min([self.DFSMiniMax(successor[0], (agentIndex + 1) % (self.numGhosts + 1), (currentDepth + 1) if (agentIndex == self.numGhosts) else currentDepth) for successor in successors])



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


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
        util.raiseNotDefined()


def genericEvaluationFunction(currentGameState, coefficients):
    # The state corresponds to a terminal node
    if currentGameState.isWin():
        return INF             # utility(t) = +inf
    if currentGameState.isLose():
        return NEGATIVE_INF    # utility(t) = -inf

    # The current game score
    # Usefull to avoid Pacman "stopping" or doing useless move when the other params are close
    gameScore = scoreEvaluationFunction(currentGameState)

    # Distance to the closest food
    # TODO : to improve the eval function, return the path to go there and check if there is no ghost on it
    distClosestFood = getDistClosestFood(currentGameState)

    # Distance to the closest unscared ghost and to the closest scared ghost
    # Note that closest unscared ghost must be reachable (checking the timer of scare)
    (distClosestUnscaredGhost, distClosestScaredGhost) = getDistClosestGhost(currentGameState)

    if (distClosestScaredGhost != 0):
        distClosestScaredGhost = 1.0/distClosestScaredGhost

    # Basic info about the remaining food and capsules
    foodLeft = currentGameState.getNumFood()
    capsulesLeft = len(currentGameState.getCapsules())

    # Linear combination of all those elements, COEF are found groping
    score = coefficients['COEF_gameScore'] * gameScore + \
            coefficients['COEF_distClosestFood'] * distClosestFood + \
            coefficients['COEF_distClosestUnscaredGhost'] * distClosestUnscaredGhost + \
            coefficients['COEF_distClosestScaredGhost'] * distClosestScaredGhost + \
            coefficients['COEF_foodLeft'] * foodLeft + \
            coefficients['COEF_capsulesLeft'] * capsulesLeft

    return score


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # To improve the coefficients we could have used some machine learning algorithms (genetic programming, svm, etc.)
    coefficients = {}
    coefficients['COEF_gameScore'] = 1
    coefficients['COEF_distClosestFood'] = -1.5
    coefficients['COEF_distClosestUnscaredGhost'] = 2
    coefficients['COEF_distClosestScaredGhost'] = 2000
    coefficients['COEF_foodLeft'] = -5
    coefficients['COEF_capsulesLeft'] = -10

    return genericEvaluationFunction(gameState, coefficients)

# Abbreviation
better = betterEvaluationFunction
