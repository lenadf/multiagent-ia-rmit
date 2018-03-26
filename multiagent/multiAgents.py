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
    score = 0

    for x in range(food.width):
        for y in range(food.height):
            if food[x][y] == True:
                dist += util.manhattanDistance(pos, (x, y))

    for x in range(2):
        for y in range(2):
            if food[x][y] == True:
                scoreFood = 50

    return (dist, score)

def getScoreFood(currentGameState, successorGameState):

    newPos = successorGameState.getPacmanPosition()
    scoreFood = 0
    (x,y) = newPos
    #(a,b) = distToFood(curengame)

    food = currentGameState.getFood()

    (oldDistToFood, oldCloseFood) = distToFood(currentGameState)
    (newDistToFood, newCloseFood) = distToFood(successorGameState)

    #print "old to food:",oldDistToFood
    #print "new to food:",newDistToFood

    if food[x][y]:
        scoreFood += 15

    if (x, y) in currentGameState.getCapsules():
        scoreFood += 200

    if oldDistToFood > newDistToFood:
        scoreFood += 50
    else:
        scoreFood -= 50

    scoreFood += newCloseFood

    return scoreFood

def isOnCollisionRoad(currentGameState, newDist, pos, newPos, ghost, scaredTimes):

    score = 0

    print "SA MERE"

    #pos = currentGameState.getPacmanPosition()
    dir = currentGameState.getPacmanState().getDirection()
    #ghostStates = currentGameState.getGhostStates()
    #newPos = successorGameState.getPacmanPosition()

    #for ghost in ghostStates:

        #newDist = util.manhattanDistance(newPos, ghost.getPosition())
    ghostDir = ghost.getDirection()
    ghostPos = ghost.getPosition()

    #print "new dist:",newDist

    if (newDist <= 4):

        for time in scaredTimes:

            if time == 0:

                if (dir == 'South') and ((ghostDir == 'East') or (ghostDir == 'West')):
                    if pos[1] > ghostPos[1]:
                        print "La merde"
                        score -= 100
                    #else:
                        #score += 0

                if (dir == 'North') and ((ghostDir == 'East') or (ghostDir == 'West')):
                    if pos[1] < ghostPos[1]:
                        print "La merde"
                        score -= 100
                    #else:
                        #score += 50

                if (dir == 'West') and ((ghostDir == 'North') or (ghostDir == 'South')):
                    if pos[0] > ghostPos[0]:
                        print "La merde"
                        score -= 100
                    #else:
                        #score += 50

                if (dir == 'East') and ((ghostDir == 'North') or (ghostDir == 'South')):
                    if pos[0] < ghostPos[0]:
                        print "La merde"
                        score -= 100
                    #else:
                        #score += 50

                if (((dir == 'West') and (ghostDir == 'East')) or ((dir == 'East') and (ghostDir == 'West'))) and (dir[0] == ghostDir[0]):
                    score -= 200

                #if (((dir == 'West') and (ghostDir == 'West')) or ((dir == 'East') and (ghostDir == 'East'))) and (dir[0] == ghostDir[0]):
                #    score -= 50

                if (((dir == 'North') and (ghostDir == 'South')) or ((dir == 'South') and (ghostDir == 'North'))) and (dir[1] == ghostDir[1]):
                    score -= 200

                #if (((dir == 'North') and (ghostDir == 'North')) or ((dir == 'South') and (ghostDir == 'South'))) and (dir[1] == ghostDir[1]):
                #    score -= 50

    return score

def getScoreGhosts(currentGameState, successorGameState):

    scoreGhost = 0

    ghostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    pos = currentGameState.getPacmanPosition()
    newPos = successorGameState.getPacmanPosition()

    for ghost in ghostStates:
        oldDist = util.manhattanDistance(pos, ghost.getPosition())
        newDist = util.manhattanDistance(newPos, ghost.getPosition())

        print "new distance:",newDist

        for time in newScaredTimes:
            if time > 3:
                if newDist >= oldDist:
                    #Going away from the ghosts
                    scoreGhost -= 100
                else:
                    #Getting closer to the ghosts
                    scoreGhost += 200

        if newDist >= oldDist:
            #Going away from the ghosts
            scoreGhost += 50
        else:
            #Getting closer to the ghosts
            scoreGhost -= 50

        scoreGhost += isOnCollisionRoad(currentGameState, newDist, pos, newPos, ghost, newScaredTimes)


    #dir = currentGameState.getPacmanState().getDirection()

    #ghostStates = currentGameState.getGhostStates()

    #newGhostStates = successorGameState.getGhostStates() #Tableau
    #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] #Tableau




    """
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

    #print "Score scoreGhosts:",scoreGhost
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

        #isOnCollisionRoad(currentGameState, successorGameState)

        foodList = newFood.asList()

        score = 0

        print "currentGameState:",currentGameState
        print "SuccessorGameState:", successorGameState
        print "newPos:", newPos
        print "newFood:",newFood
        print "newGhostStates:",newGhostStates[0]
        print "newScaredTimes:",newScaredTimes

        """
        (x, y) = newPos

        food = currentGameState.getFood()

        oldDistToFood = distToFood(currentGameState)
        newDistToFood = distToFood(successorGameState)

        print "old to food:",oldDistToFood
        print "new to food:",newDistToFood

        if food[x][y]:
            score += 15

        if (x, y) in currentGameState.getCapsules():
            score += 200

        if oldDistToFood > newDistToFood:
            score += 50
        else:
            score -= 30

        """

        if newPos == (0,0):
            print "A L'ARRET"
            score -=100

        score = score + getScoreGhosts(currentGameState, successorGameState) + getScoreFood(currentGameState, successorGameState)


        """
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
        """

        print "Score coucou:",score

        return score #successorGameState.getScore()


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
