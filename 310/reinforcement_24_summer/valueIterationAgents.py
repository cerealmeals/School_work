# valueIterationAgents.py
# -----------------------
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
import queue

# valueIterationAgents.py
# -----------------------
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


import mdp, util, random
from queue import PriorityQueue

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def getGreedyUpdate(self, state):
        """computes a one step-ahead value update and return it"""
        if self.mdp.isTerminal(state):
            return self.values[state]
        actions = self.mdp.getPossibleActions(state)
        vals = util.Counter()
        for action in actions:
            vals[action] = self.computeQValueFromValues(state, action)
        return max(vals.values())

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        currIterations = 0
        while currIterations < self.iterations:
            # initialize a counter to keep track of our values per iteration
            allVals = util.Counter()
            possStates = self.mdp.getStates()
            for state in possStates:
                # if there are no actions don't iterate, else compute
                if not self.mdp.isTerminal(state):
                    # initialize counter for getting values from the current state
                    vals = util.Counter()
                    possActions = self.mdp.getPossibleActions(state)
                    # iterate over actions and get their qvalues
                    for action in possActions:
                        vals[action] = self.computeQValueFromValues(state, action)
                    # get the best seen value for that state and action
                    allVals[state] = max(vals.values())
            currIterations += 1
            # update the policy with the best values
            self.values = allVals.copy()

        # values1 = util.Counter()
        # for i in range(self.iterations):
        #     print(i, " interation of runValueIteration")
        #     for state in self.mdp.getStates():
        #         values1[state] = self.values[state]


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        list_of_nextState_and_prob = self.mdp.getTransitionStatesAndProbs(state, action)

        value = 0
        for tup in list_of_nextState_and_prob:
            value += (((self.values[tup[0]]* self.discount) + self.mdp.getReward(state, action, tup[0])) * tup[1])

        return value


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        
        actions = self.mdp.getPossibleActions(state)
        highest = float('-inf')
        return_action = actions[0]
        for action in actions:
            value = self.computeQValueFromValues(state, action)
            if value > highest:
                highest = value
                return_action = action
            elif value == highest:
                if 0.5 > random.random():
                    highest = value
                    return_action = action
        return return_action


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)


    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        #compute predecessors of all states
        predecessors = util.Counter() # []
        for state in self.mdp.getStates():
            predecessors[state] = set()

        for state in self.mdp.getStates():
            possible_action = self.mdp.getPossibleActions(state)
            for action in possible_action:
                nextState_prob_list = self.mdp.getTransitionStatesAndProbs(state, action)
                for tuple in nextState_prob_list:
                    if tuple[1] > 0:
                        predecessors[tuple[0]].add(state)

        # setup priority queue for all states based on their highest diff in greedy update
        PrioQueue = util.PriorityQueue()
        possStates = self.mdp.getStates()
        for state in possStates:
            if not self.mdp.isTerminal(state):
                value = abs(self.values[state] - self.getGreedyUpdate(state))
                PrioQueue.push(state, -value)

        # run priority sweeping value iteration:
        for i in range(self.iterations):
            if PrioQueue.isEmpty():
                return
            state = PrioQueue.pop()
            if not self.mdp.isTerminal(state):
                self.values[state] = self.getGreedyUpdate(state)
            
            for predecessor_state in predecessors[state]:
                value = abs(self.values[predecessor_state] - self.getGreedyUpdate(predecessor_state))
                if value > self.theta:
                    PrioQueue.update(predecessor_state, -value)
        



class AsynchronousValueIterationAgent:
    print("Not part of this assignment.")
    pass
