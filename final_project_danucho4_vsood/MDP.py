'''MDP.py
Jose Daniel Gil Chavez, Vishesh Sood
CSE 415
Final Project

MDP File to Support 2X2 Rubik's Cube

Provides representations for Markov Decision Processes and Q-learning
exploration.

The transition function should be a function of three arguments:
T(s, a, sp), where s and sp are states and a is an action.
The reward function should also be a function of the three same
arguments.  However, its return value is not a probability but
a numeric reward value -- any real number.

operators:  state-space search objects consisting of a precondition
 and deterministic state-transformation function.
 We assume these are in the "QUIET" format used in earlier assignments.

actions:  objects (for us just Python strings) that are
 mapped to the operators through the registered field.
'''
import random

REPORTING = True

class MDP:
    def __init__(self):
        self.known_states = set()
        self.succ = {} # hash of adjacency lists by state.

    # all register functions gets the required functionallity for the
    # given "World"

    def register_start_state(self, start_state):
        self.start_state = start_state
        self.known_states.add(str(start_state))

    def register_goal_state(self, goal_state):
        self.goal_state = goal_state

    def register_goal_test(self, goal_test):
        self.goal_test = goal_test

    def register_actions(self, action_list):
        self.actions = action_list

    def register_action_to_op(self, action_to_op):
        self.action_to_op = action_to_op

    def register_describe_state(self, ds):
        self.describe_state = ds

    def register_operators(self, op_list):
        self.ops = op_list

    def register_transition_function(self, transition_function):
        self.T = transition_function

    def register_reward_function(self, reward_function):
        self.R = reward_function

    def state_neighbors(self, state):
        '''Return a list of the successors of state.  First check
           in the hash self.succ for these.  If there is no list for
           this state, then construct and save it.
           And then return the neighbors.'''
        neighbors = self.succ.get(str(state), False)
        if neighbors==False:
            neighbors = []
            for op in self.ops:
                print(op.name)
                neighbors.append(op.apply(state))
            self.succ[str(state)]=neighbors
            for neighbor in neighbors:
                self.known_states.add(str(neighbor))
        return neighbors


    # updates the current state to the resulting state of applying the given
    # action to the current state
    def take_action(self, a):
        s = self.current_state
        sp = self.action_to_op.get(a).apply(s)
        r = self.R(s, a, sp)
        self.current_state = sp
        self.describe_state(self.current_state)
        if REPORTING: print("After action "+a+", moving to state "+str(sp)+\
                           "; reward is "+str(r))

    # finds all the possible states and saves them
    def generateAllStates(self):
        self.IterativeDFS(self.start_state)
        # for s in self.known_states:
        #     print(s)
        # print(len(self.known_states))


    # performs Q learning for the number
    def QLearning(self, discount, nEpisodes, epsilon):
        self.QValues = {}
        self.N = {}
        # initialize QValues to 0:
        for state in self.known_states:
            for action in self.actions:
                self.QValues[(state, action)] = 0
                self.N[(state, action)] = 0
        for i in range(nEpisodes):
            self.current_state = self.start_state
            while True:
                s = self.current_state
                a = self.decideAction(s, epsilon)
                self.N[(str(s), a)] += 1
                self.QValues[(str(s), a)] = self.Q(str(s), a, discount, epsilon)
                if self.goal_test(self.current_state):
                    break


    # calculates the alpha leaning rate
    def alpha(self, state, action):
        return 1 / self.N.get((str(state), action))


    # retuns the name of the best possible action for the given state
    def getMaxAction(self, state):
        max_action = ""
        max = -10000
        for action in self.actions:
            action_val = self.QValues.get((str(state), action))
            if max < action_val:
                max = action_val
                max_action = action
        return max_action


    # returns the value of the Q function for the bellman equation
    def Q(self, s, a, discount, epsilon):
        QVal = self.QValues.get((str(s), a))
        alpha = self.alpha(s, a)
        self.take_action(a)
        sp = self.current_state
        sp_max_action = self.getMaxAction(sp)
        T = self.T(s, a, sp)
        sample = self.R(s, a, sp) + discount * self.QValues.get((str(sp), sp_max_action))
        value = (1 - alpha) * QVal + alpha * sample
        if T == 0:
            self.current_state = s
            value = QVal
        print("Value = ", value)
        #self.describe_state(eval(s))
        #print("Value for S:", s, " ", value)
        return value

    # decide to take the optimal action, or explore a new path
    # according to the greedy epsilon learning
    def decideAction(self, state, epsilon):
        rnd = random.uniform(0.0, 1.0)
        if rnd < epsilon:
            action_num = random.randint(0, 4)
            return self.actions[action_num]
        else:
            return self.getMaxAction(state)

    # creates a dictionary that maps every state with its best possible action
    def extractPolicy(self):
        self.optPolicy = {}
        for state in self.known_states:
            max_action = self.getMaxAction(state)
            self.optPolicy[state] = max_action

    # iterative Depth first search to find every state
    def IterativeDFS(self, initial_state):
        OPEN = [initial_state]
        CLOSED = []

        while OPEN != []:
            S = OPEN[0]
            del OPEN[0]
            CLOSED.append(S)
            L = self.state_neighbors(S)
            for state in L:
               if state not in CLOSED:
                   OPEN.append(state)