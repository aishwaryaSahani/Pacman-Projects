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
from pip._internal.utils.outdated import SELFCHECK_DATE_FMT

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
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
#         
#         print newPos
#         print newFood
#         print newGhostStates
#         print newScaredTimes
#        
        foodCount = successorGameState.getNumFood() 
        
        oldFoodCount=currentGameState.getNumFood()

#         Maximize ghost distance
        ghostDist = 0.0
        ghost = successorGameState.getGhostPositions()
        ghostHeuristic =  manhattanDistance(newPos, ghost[0])
        if(ghostHeuristic ==0):
            ghostHeuristic =0.01
        ghostDist = 1.0/ghostHeuristic
        
#         Minimize food distance
        result = 99.0
        foodDist =0.0 
        
        for food in newFood.asList():
            foodHeuristic =  manhattanDistance(newPos, food)
            if(foodHeuristic<result):
                result = foodHeuristic
        if(result ==99):
            result =1
        foodDist = 1.0/result
        
#         Minimize capsule distance
        result = 99.0
        capDist =0.0 
 
        capsulePosition = successorGameState.getCapsules()
        for power in capsulePosition:
            powerHeuristic =  manhattanDistance(newPos, power)
            if(powerHeuristic<result):
                result = powerHeuristic
        if(result ==99):
            result =1
        if(result == 0):
            if(newScaredTimes[0]>1):
                ghostDist = -1*ghostDist
        capDist = 1.0/result
       
        return successorGameState.getScore() + foodDist - ghostDist + oldFoodCount - foodCount + capDist + newScaredTimes[0]
    
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
#         print self.depth
#         print gameState.getNumAgents()
#         print gameState.getLegalActions(0)
        
        score, bestAction = self.value(gameState, 0, 0)
         
        return bestAction
    
    def value(self, gameState, depth, agent):
        if(gameState.isWin() or gameState.isLose() or depth == self.depth):
            return self.evaluationFunction(gameState), None
        
        if agent==0:
            score, bestAction = self.maxAgent(gameState, depth)
        else:
            score, bestAction = self.minAgent(gameState, depth, agent)
        return score, bestAction 
        
    
    def maxAgent(self, gameState, depth):
          
        maxScore = -99999
        bestAction =None
        
        agentLegalMoves = gameState.getLegalActions(0)
        
        if(len(agentLegalMoves)==0):
            return self.evaluationFunction(gameState), None
        
        for action in agentLegalMoves:
            successor = gameState.generateSuccessor(0, action)
            score, act = self.value(successor, depth, 1)
            if score > maxScore:
                maxScore = score
                bestAction = action
        return maxScore, bestAction   
    
    def minAgent(self, gameState, depth, agent):   
          
        minScore = 99999
        bestAction =None

        agentLegalMoves = gameState.getLegalActions(agent)
        if(len(agentLegalMoves)==0):
            return self.evaluationFunction(gameState), None
        
        for action in agentLegalMoves:
            successor = gameState.generateSuccessor(agent, action)
            
            if agent+1 < gameState.getNumAgents():
                score,act  = self.value(successor, depth, agent+1)
            else:
                score,act = self.value(successor, depth+1, 0)
            if score < minScore:
                minScore = score
        return minScore, None   
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        score, bestAction = self.value(gameState, 0, 0, -99999, 99999)
         
        return bestAction
    
    def value(self, gameState, depth, agent, alpha, beta):
        if(gameState.isWin() or gameState.isLose() or depth == self.depth):
            return self.evaluationFunction(gameState), None
        
        if agent==0:
            score, bestAction = self.maxAgent(gameState, depth, alpha, beta)
        else:
            score, bestAction = self.minAgent(gameState, depth, agent, alpha, beta)
        return score, bestAction 
        
    
    def maxAgent(self, gameState, depth, alpha, beta):
        
        if(gameState.isWin() or gameState.isLose() or depth == self.depth):
            return self.evaluationFunction(gameState), None
      
        maxScore = -99999
        bestAction =None
        
        agentLegalMoves = gameState.getLegalActions(0)
        
        if(len(agentLegalMoves)==0):
            return self.evaluationFunction(gameState), None
        
        for action in agentLegalMoves:
            successor = gameState.generateSuccessor(0, action)
            score,act = self.value(successor, depth, 1, alpha, beta)
            if score > maxScore:
                maxScore = score
                bestAction = action
                
            if(maxScore>beta):
                return maxScore, bestAction
            alpha = max(alpha,maxScore)
        return maxScore, bestAction   
    
    def minAgent(self, gameState, depth, agent, alpha, beta):   
        
        minScore = 99999
        bestAction =None

        agentLegalMoves = gameState.getLegalActions(agent)
        if(len(agentLegalMoves)==0):
            return self.evaluationFunction(gameState), None
        
        for action in agentLegalMoves:
            successor = gameState.generateSuccessor(agent, action)
            
            if agent+1 < gameState.getNumAgents():
                score, act  = self.value(successor, depth, agent+1, alpha, beta)
            else:
                score,act = self.value(successor, depth+1, 0, alpha, beta)
            if score < minScore:
                minScore = score
           
            if(minScore<alpha):
                return minScore, None
            beta = min(beta,minScore)
        return minScore, None
        

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
        
        score, bestAction = self.value(gameState, 0, 0)
         
        return bestAction
    
    def value(self, gameState, depth, agent):
        if(gameState.isWin() or gameState.isLose() or depth == self.depth):
            return self.evaluationFunction(gameState), None
        
        if agent==0:
            score, bestAction = self.maxAgent(gameState, depth)
        else:
            score, bestAction = self.expectiMaxAgent(gameState, depth, agent)
        return score, bestAction 
        
    
    def maxAgent(self, gameState, depth):
          
        maxScore = -99999
        bestAction =None
        
        agentLegalMoves = gameState.getLegalActions(0)
        
        if(len(agentLegalMoves)==0):
            return self.evaluationFunction(gameState), None
        
        for action in agentLegalMoves:
            successor = gameState.generateSuccessor(0, action)
            score, act = self.value(successor, depth, 1)
            if score > maxScore:
                maxScore = score
                bestAction = action
        return maxScore, bestAction   
    
    def expectiMaxAgent(self, gameState, depth, agent):   
          
        minScore = 0
        bestAction =None

        agentLegalMoves = gameState.getLegalActions(agent)
        if(len(agentLegalMoves)==0):
            return self.evaluationFunction(gameState), None
        prob = 1.0/len(agentLegalMoves)
        for action in agentLegalMoves:
            
            successor = gameState.generateSuccessor(agent, action)
            
            if agent+1 < gameState.getNumAgents():
                score,act  = self.value(successor, depth, agent+1)
            else:
                score,act = self.value(successor, depth+1, 0)
            minScore += prob*score
        return minScore, None   
    
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    
    foodCount = currentGameState.getNumFood() 
    
    oldFoodCount=currentGameState.getNumFood()
    
    #         Maximize ghost distance
    ghostDist = 0.0
    ghost = currentGameState.getGhostPositions()
    ghostHeuristic =  manhattanDistance(newPos, ghost[0])
    if(ghostHeuristic ==0):
        ghostHeuristic =0.01
    ghostDist = 1.0/ghostHeuristic
    
    #         Minimize food distance
    result = 99.0
    foodDist =0.0 
    
    for food in newFood.asList():
        foodHeuristic =  manhattanDistance(newPos, food)
        if(foodHeuristic<result):
            result = foodHeuristic
    if(result ==99):
        result =1
    foodDist = 1.0/result
    
    #         Minimize capsule distance
    result = 99.0
    capDist =0.0 
    
    capsulePosition = currentGameState.getCapsules()
    for power in capsulePosition:
        powerHeuristic =  manhattanDistance(newPos, power)
        if(powerHeuristic<result):
            result = powerHeuristic
    if(result ==99):
        result =1
    if(result == 0):
        if(newScaredTimes[0]>1):
            ghostDist = -1*ghostDist
    capDist = 1.0/result
    
    return currentGameState.getScore() + foodDist - ghostDist + oldFoodCount - foodCount + capDist + newScaredTimes[0]


# Abbreviation
better = betterEvaluationFunction

