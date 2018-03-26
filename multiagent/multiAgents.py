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

def distToFood(gameState):

    pos = gameState.getPacmanPosition()
    food = gameState.getFood()
    dist = 0

    for x in range(food.width):
        for y in range(food.height):
            if food[x][y] == True:
                dist += util.manhattanDistance(pos, (x, y))


    print "distToFood:",dist
    return dist


def isOnCollisionRoad(currentGameState, successorGameState):

    score = 0

    pos = currentGameState.getPacmanPosition()
    dir = currentGameState.getPacmanState().getDirection()
    ghostStates = currentGameState.getGhostStates()
    newPos = successorGameState.getPacmanPosition()

    for ghost in ghostStates:

        newDist = util.manhattanDistance(newPos, ghost.getPosition())
        ghostDir = ghost.getDirection()
        ghostPos = ghost.getPosition()

        if (newDist <= 5):

            if (dir == 'South') and ((ghostDir == 'East') or (ghostDir == 'West')):
                if pos[1] > ghostPos[1]:
                    print "La merde"
                    score -= 25

            if (dir == 'North') and ((ghostDir == 'East') or (ghostDir == 'West')):
                if pos[1] < ghostPos[1]:
                    print "La merde"
                    score -= 25

            if (dir == 'West') and ((ghostDir == 'North') or (ghostdir == 'South')):
                if pos[0] > ghostPos[0]:
                    print "La merde"
                    score -= 25

            if (dir == 'East') and ((ghostDir == 'North') or (ghostDir == 'South')):
                if pos[0] < ghostPos[0]:
                    print "La merde"
                    score -= 25







def getScoreGhosts(currentGameState, successorGameState):
    scoreGhost = 0

    pos = currentGameState.getPacmanPosition()
    dir = currentGameState.getPacmanState().getDirection()

    ghostStates = currentGameState.getGhostStates()

    newPos = successorGameState.getPacmanPosition()
    newGhostStates = successorGameState.getGhostStates() #Tableau
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] #Tableau





    for ghost in ghostStates:

        #ghost and newGhost are the same
        #oldDist = util.manhattanDistance(pos, ghost.getPosition())
        newDist = util.manhattanDistance(newPos, ghost.getPosition())

        ghostDir = ghost.getDirection()

        if (newDist <= 5):

            if ((dir == 'West') and (ghostDir == 'East') or (dir == 'East') and (ghostDir == 'West')) and (dir[0] == ghostDir[0]):
                scoreGhost -= 100


            if ((dir == 'North') and (ghostDir == 'South') or (dir == 'South') and (ghostDir == 'North')) and (dir[1] == ghostDir[1]):
                scoreGhost -=100

        """
        if newDist >= oldDist:
            #Going away from the ghosts
            scoreGhost += 50
        else:
            #Getting closer to the ghosts
            scoreGhost -= 50
        """
        #print oldDist
        #print newDist

    print "Score scoreGhosts:",scoreGhost
    return scoreGhost


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

        isOnCollisionRoad(currentGameState)

        score = 0

        print "currentGameState:",currentGameState
        print "SuccessorGameState:", successorGameState
        print "newPos:", newPos
        print "newFood:",newFood
        print "newGhostStates:",newGhostStates[0]
        print "newScaredTimes:",newScaredTimes

        (x, y) = newPos
        food = currentGameState.getFood()

        if food[x][y]:
            score += 10

        if (x, y) in currentGameState.getCapsules():
            print "EHyyyyyyyyy"
            score += 50

        for ghost in newGhostStates:
            dir = currentGameState.getPacmanState().getDirection()
            #ghost and newGhost are the same
            newDist = util.manhattanDistance(newPos, ghost.getPosition())

            ghostDir = ghost.getDirection()

            if (newDist <= 5):

                if ((dir == 'West') and (ghostDir == 'East') or (dir == 'East') and (ghostDir == 'West')) and (dir[0] == ghostDir[0]):
                    score -= 100


                if ((dir == 'North') and (ghostDir == 'South') or (dir == 'South') and (ghostDir == 'North')) and (dir[1] == ghostDir[1]):
                    score -=100


        print "Score coucou:",score

        return successorGameState.getScore()


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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
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
        util.raiseNotDefined()

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
