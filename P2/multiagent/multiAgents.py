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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        #print((bestIndices))

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
        manhattansFood = []
        for food in newFood.asList():
            s = manhattanDistance(newPos,food)
            manhattansFood.append(s)
        fsFood = 999
        if(len(manhattansFood) != 0):
            fsFood = min(manhattansFood)
        # manhattansGhost = []
        # fsGhost = 0
        fs = 0
        for ghost in newGhostStates:
            s = manhattanDistance(newPos,ghost.getPosition())
            fs += max(5-s,0)
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        if (newScaredTimes[0] != 0):
            return successorGameState.getScore() + 4/fsFood - (fs)
        elif (newScaredTimes[0] == 0 and newPos == newGhostStates[0].getPosition()):
            print(newPos)
            return successorGameState.getScore() - 4/fsFood - (fs*8)
        else:
            return successorGameState.getScore() + 4/fsFood - (fs*2)
        print(newPos)
        # print(newGhostStates[0].getPosition())
        print(newFood.asList())
        #print(newScaredTimes[0])

        "*** YOUR CODE HERE ***"
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
    def pacman(self,gameState, depth): # max agent
        actions = gameState.getLegalActions(0)
        evals = {}
        if (len(actions) != 0):
            evals = {-9999:actions[0]}
        if (gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        else:
            for action in actions:
                s = self.ghosts(gameState.generateSuccessor(0,action),depth,1)
                evals[s] = action
                maxScore = max(evals)
            if depth == 0:
                return evals[maxScore]
            else:
                return maxScore

    def ghosts(self,gameState, depth, i): # min agent
        if (gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        elif(i < gameState.getNumAgents()-1):
            actions = gameState.getLegalActions(i)
            s = 9999
            evals = [s]
            for action in actions:
                s = self.ghosts(gameState.generateSuccessor(i,action), depth, i+1)
                evals.append(s)
            return min(evals)
        elif(i == gameState.getNumAgents()-1):
            actions = gameState.getLegalActions(i)
            s = 9999
            evals = [s]
            for action in actions:
                if (depth == self.depth-1):
                    s = self.evaluationFunction(gameState.generateSuccessor(i,action))
                else:
                    s = self.pacman(gameState.generateSuccessor(i, action),depth+1)
                evals.append(s)
            return min(evals)
        else:
            return
    
    def getAction(self, gameState):
        #print(gameState.getLegalActions(0))
        #print(gameState.getNumAgents())
        
        return self.pacman(gameState, self.index)
             
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
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def pacman(self,gameState, depth, alpha, beta): # max agent
        actions = gameState.getLegalActions(0)
        bestAct = None
        value = -999999999
        if (gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        else:
            for action in actions:
                value = max(value, self.ghosts(gameState.generateSuccessor(0,action),depth,1, alpha, beta))
                if (self.ghosts(gameState.generateSuccessor(0,action),depth,1, alpha, beta) >= value):
                    bestAct = action
                if (value > beta):
                    return value
                alpha = max(alpha, value)
            if depth == 0:
                return bestAct
            else:
                return value

    def ghosts(self,gameState, depth, i, alpha, beta): # min agent
        value = 999999999
        if (gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        elif(i < gameState.getNumAgents()-1):
            actions = gameState.getLegalActions(i)
            for action in actions:
                value = min(self.ghosts(gameState.generateSuccessor(i,action), depth, i+1, alpha,beta),value)
                if (value < alpha):
                    return value
                beta = min(beta, value)
            return value
        elif(i == gameState.getNumAgents()-1):
            actions = gameState.getLegalActions(i)
            for action in actions:
                if (depth == self.depth-1):
                    value = min(self.evaluationFunction(gameState.generateSuccessor(i,action)),value)
                else:
                    value = min(self.pacman(gameState.generateSuccessor(i, action),depth+1,alpha, beta),value)
                if (value < alpha):
                    return value
                beta = min(beta, value)
            return value
        else:
            return

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        return self.pacman(gameState, self.index, -9999999, 9999999)

        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def pacman(self,gameState, depth): # max agent
        actions = gameState.getLegalActions(0)
        bestAct = None
        value = -999999999
        if (gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        else:
            for action in actions:
                s = self.ghosts(gameState.generateSuccessor(0,action),depth,1)
                value = max(value, s)
                if (s >= value):
                    bestAct = action
            if depth == 0:
                return bestAct
            else:
                return value

    def ghosts(self,gameState, depth, i): # min agent
        if (gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        elif(i < gameState.getNumAgents()-1):
            actions = gameState.getLegalActions(i)
            s = 9999
            evals = []
            for action in actions:
                s = self.ghosts(gameState.generateSuccessor(i,action), depth, i+1)
                evals.append(s)
            return (sum(evals)) / (len(evals))
        elif(i == gameState.getNumAgents()-1):
            actions = gameState.getLegalActions(i)
            s = 9999
            evals = []
            for action in actions:
                if (depth == self.depth-1):
                    s = self.evaluationFunction(gameState.generateSuccessor(i,action))
                else:
                    s = self.pacman(gameState.generateSuccessor(i, action),depth+1)
                evals.append(s)
            return (sum(evals)) / (len(evals))
        else:
            return

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        return self.pacman(gameState, self.index)

        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <
    According to pacman's position and the manhattan ditances between pacman and the left foods, ghost and capsules
    I calculated the score by adding and decreasing the calculated paramaters to 
    the default score(currentGameState.getScore()).
    I also added the number of foods and capsules to the function whcih made a noticeable difference and
    in some cases the scores enchaned from the previous state.
    - with number of foods and capsules: 1074.0, 1226.0, 1136.0, 1151.0, 1015.0, 1131.0, 1324.0, 1170.0, 812.0, 1159.0
    - without:                           1076.0, 1023.0, 1320.0, 1133.0, 1258.0, 935.0, 899.0, 1183.0, 812.0, 971.0
    >
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    manFoods = []
    distGhost = 0
    for ghost in ghostStates:
        s = manhattanDistance(pos,ghost.getPosition())
        distGhost += max(s,distGhost)
    for food in foods:
        manFoods.append(manhattanDistance(pos,food))
    distCapsul = 99999
    for cap in currentGameState.getCapsules():
        s = manhattanDistance(pos,cap)
        distCapsul += min(s,distCapsul)

    #print(len(foods.asList()))
    #print(pos)
    #print(currentGameState.getCapsules())
    #print(foods.asList())
    #print(currentGameState.getScore())
    a = min(manFoods)
    return currentGameState.getScore() + 2/a - distGhost*10 - 10*len(foods.asList()) - distCapsul - len(currentGameState.getCapsules())*3
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
