'''rubik2x2.py
Jose Daniel Gil Chavez, Vishesh Sood
CSE 415
Final Project
This file consists of everything required to solve a 2x2 rubik's cube.
These include generating states, goal tests, generating hash codes, and
much more.

This is to be used with either A* or MDP to solve any rubik's cube.

Warning:
WE ASSUME THAT THE RUBIK'S CUBE ONLY TURNS SIDES IN 180 DEGREES.

'''
import copy
import random
import MDP

# <METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "2X2 Rubik Cube Solver"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['V. Sood', 'J. Gil Chavez']
PROBLEM_CREATION_DATE = "28-MAY-2016"
PROBLEM_DESC = \
    '''
    This formulation of the Rubik's Cube uses generic
    Python 3 constructs and has been tested with Python 3.4.
    It is designed to work according to the QUIET tools interface.
    '''
# </METADATA>

INITIAL_STATE = [[2, 2, 0, 0], [1, 1, 3, 3], [2, 2, 0, 0], [3, 3, 1, 1], [5, 4, 5, 4], [4, 5, 4, 5]]
INT_TO_COLORS = {0: 'G', 1: 'O', 2: 'B', 3: 'R', 4: 'Y', 5: 'W',}
ACTIONS = ["Up", "Down", "Left", "Right", "Front", "Back"]
OPERATORS = []
ACTION_TO_OP = {}


class Operator:
    def __init__(self, name, state_transf):
        self.name = name
        self.state_transf = state_transf

    def apply(self, s):
        return self.state_transf(s)

# createInitialState:
# This function creates the initial state, giving a scramblled cube, generates
# the operators, asks the user for the colors they wish to use and sets them,
# and then returns the state in the end.
def createInitialState():
    global INITIAL_STATE
    createOperators()
    requestColors = input("Would you like to customize the colors of your Rubik's Cube? (y/n) ")
    if requestColors is 'y':
        resetInitialStateColors()
        getUserColors()
    return INITIAL_STATE

# resetInitialState:
# This function sets the color mapping to Null, allowing it to be rewritten.
def resetInitialStateColors():
    global INT_TO_COLORS
    for i in range(6):
        INT_TO_COLORS[i] = None

# getUserColors:
# This function asks the user to enter colors and sets the mapping of the colors
# allowing it to be used when the cube is drawn on console.
def getUserColors():
    global INT_TO_COLORS
    for i in range(6):
        color = input("Please Enter Color " + str(i+1) + ": ").upper()
        while checkIfColorExists(color[0]):
            print("The color has initials that already exist")
            color = input("Please Enter Color " + str(i + 1) + ": ").upper()
        INT_TO_COLORS[i] = color[0]

# checkIfColorExists:
# This function takes a character and checks whether the color has already been
# assigned to the map. If it has, it returns true, else it returns a false.
def checkIfColorExists(char):
    global INT_TO_COLORS
    for i in range(6):
        if INT_TO_COLORS[i] == char:
            return True
    return False

# scramble:
# This function scrambles the state by running 100 random operators on the given
# state, and then returns that state as a new state.
def scramble(s):
    state = s
    for i in range (100):
        value = random.randint(0,5)
        state = OPERATORS[value].apply(state)
    return state

# deepEquals:
# This function compares two states that are passed into it and checks whether they
# are identical or not. Returns true or false respectively.
def deepEquals(state1, state2):
    for side in range(6):
        for tile in range(4):
            if state1[side][tile] != state2[side][tile]:
                return False
    return True


# hashCode:
# This function returns a hashcode for the state passed down to it.
def hashCode(state):
    return str(state)

# copyState:
# This function returns a copy of the state passed into it
def copyState(state):
    return copy.deepcopy(state)

# goalTest:
# This function takes a state and checks whether or not it is the final state, i.e.
# a completed rubik's cube.
def goalTest(s):
    for side in s:
        if len(set(side)) > 1:
            return False
    return True

# goalMessage.
# This function prints a message when the goal stage is reached and displays it
# to the user
def goalMessage():
    print("The Rubik's Cube has been solved!!")
    print("Final State: ")

# describeState
# This state takes a state and prints out a visual for the state.
def describeState(state):
    global INT_TO_COLORS
    tiles = state[4]
    print("         -------")
    for i in range(0, 4, 2):
        print("        | " + INT_TO_COLORS.get(tiles[i]) + " | " + INT_TO_COLORS.get(tiles[i + 1]) + " | ")
    print("---------------------------------")
    for i in range(0, 4, 2):
        line = "| "
        line += INT_TO_COLORS.get(state[0][i]) + " | " + INT_TO_COLORS.get(state[0][i + 1]) + " | "
        line += INT_TO_COLORS.get(state[1][i]) + " | " + INT_TO_COLORS.get(state[1][i + 1]) + " | "
        line += INT_TO_COLORS.get(state[2][i]) + " | " + INT_TO_COLORS.get(state[2][i + 1]) + " | "
        line += INT_TO_COLORS.get(state[3][i]) + " | " + INT_TO_COLORS.get(state[3][i + 1]) + " | "
        print(line)
    tiles = state[5]
    print("---------------------------------")
    for i in range(0, 4, 2):
        print("        | " + INT_TO_COLORS.get(tiles[i]) + " | " +  INT_TO_COLORS.get(tiles[i + 1]) + " | ")

    print("         -------")

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!! THE FOLLOWING ARE OPERATORS TO CARRY OUT ON THE RUBIKS CUBE !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def left(state):
    s = copyState(state)
    indices = [0, 1, 2]
    rotation = [5, 3, 4, 1]
    last_update = [s[1][0], s[1][2]]
    for i in range(3, 0, -1):
        if rotation[i] == 3:
            s[rotation[i]][3] = s[rotation[i - 1]][0]
            s[rotation[i]][1] = s[rotation[i - 1]][2]
        elif rotation[i] == 4:
            s[rotation[i]][0] = s[rotation[i - 1]][3]
            s[rotation[i]][2] = s[rotation[i - 1]][1]
        else:
            s[rotation[i]][0] = s[rotation[i - 1]][0]
            s[rotation[i]][2] = s[rotation[i - 1]][2]
    s[5][0] = last_update[0]
    s[5][2] = last_update[1]
    temp = s[0][0]
    s[0][0] = s[0][2]
    s[0][2] = s[0][3]
    s[0][3] = s[0][1]
    s[0][1] = temp
    return s


def right(state):
    s = copyState(state)
    indices = [0, 1, 2]
    rotation = [4, 3, 5, 1]
    last_update = [s[1][1], s[1][3]]
    for i in range(3, 0, -1):
        if rotation[i] == 3:
            s[rotation[i]][2] = s[rotation[i - 1]][1]
            s[rotation[i]][0] = s[rotation[i - 1]][3]
        elif rotation[i] == 5:
            s[rotation[i]][1] = s[rotation[i - 1]][2]
            s[rotation[i]][3] = s[rotation[i - 1]][0]
        else:
            s[rotation[i]][1] = s[rotation[i - 1]][1]
            s[rotation[i]][3] = s[rotation[i - 1]][3]
    s[4][1] = last_update[0]
    s[4][3] = last_update[1]
    temp = s[2][0]
    s[2][0] = s[2][2]
    s[2][2] = s[2][3]
    s[2][3] = s[2][1]
    s[2][1] = temp
    return s

def up(state):
    s = copyState(state)
    indices = [0, 1, 2]
    rotation = [3, 2, 1, 0]
    last_update = [s[0][0], s[0][1]]
    for i in range(3, 0, -1):
        s[rotation[i]][0] = s[rotation[i - 1]][0]
        s[rotation[i]][1] = s[rotation[i - 1]][1]
    s[3][0] = last_update[0]
    s[3][1] = last_update[1]
    temp = s[4][0]
    s[4][0] = s[4][2]
    s[4][2] = s[4][3]
    s[4][3] = s[4][1]
    s[4][1] = temp
    return s

def down(state):
    s = copyState(state)
    rotation = [1, 2, 3, 0]
    last_update = [s[0][2], s[0][3]]
    for i in range(3, 0, -1):
        s[rotation[i]][2] = s[rotation[i - 1]][2]
        s[rotation[i]][3] = s[rotation[i - 1]][3]
    s[1][2] = last_update[0]
    s[1][3] = last_update[1]
    temp = s[5][0]
    s[5][0] = s[5][2]
    s[5][2] = s[5][3]
    s[5][3] = s[5][1]
    s[5][1] = temp
    return s

def front(state):
    s = copyState(state)
    last_update = [s[5][0], s[5][1]]
    temp = s[1][0]
    s[1][0] = s[1][2]
    s[1][2] = s[1][3]
    s[1][3] = s[1][1]
    s[1][1] = temp
    # Get values from 2 and put into 5
    s[5][0] = s[2][2]
    s[5][1] = s[2][0]
    # Get values from 4 and put into 2
    s[2][0] = s[4][2]
    s[2][2] = s[4][3]
    # Get values from 0 and put into 4
    s[4][3] = s[0][1]
    s[4][2] = s[0][3]
    # Get values from 5 and put into 0
    s[0][1] = last_update[0]
    s[0][3] = last_update[1]
    return s

def back(state):
    s = copyState(state)
    last_update = [s[4][0], s[4][1]]
    temp = s[3][0]
    s[3][0] = s[3][2]
    s[3][2] = s[3][3]
    s[3][3] = s[3][1]
    s[3][1] = temp
    # 2 go to 4
    s[4][0] = s[2][1]
    s[4][1] = s[2][3]
    # 5 goes to 2
    s[2][1] = s[5][3]
    s[2][3] = s[5][2]
    # 0 goes to 5
    s[5][2] = s[0][0]
    s[5][3] = s[0][2]
    # 4 goes to 0
    s[0][0] = last_update[1]
    s[0][2] = last_update[0]
    return s


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!    THE FOLLOWING ARE OUR HEURISTICS FOR THE RUBIKS CUBE     !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def h_side(s):
    value = 0
    for tile in s[0]:
        if tile == 0:
            value += 1
    for tile in s[1]:
        if tile == 1:
            value += 1
    for tile in s[2]:
        if tile == 2:
            value += 1
    for tile in s[3]:
        if tile == 3:
            value += 1
    for tile in s[4]:
        if tile == 4:
            value += 1
    for tile in s[5]:
        if tile == 5:
            value += 1

    return value

def h_layer(s):
    value = 0
    for tile in s[5]:
        if tile == 5:
            value += 1

    greenList = s[0][-3:]
    orangeList = s[1][-3:]
    blueList = s[2][-3:]
    redList = s[3][-3:]

    count = 0
    for val in greenList:
        if val == 0:
            value += 1
            count += 1

    if count == 3:
        value += 3

    count = 0
    for val in orangeList:
        if val == 1:
            value += 1
            count += 1

    if count == 3:
        value += 3

    count = 0
    for val in blueList:
        if val == 2:
            value += 1
            count += 1

    if count == 3:
        value += 3

    count = 0
    for val in redList:
        if val == 3:
            value += 1
            count += 1

    if count == 3:
        value += 3

    for tile in s[4]:
        if tile == 4:
            value += 1

    return value


# initializes operators and its mapping
def createOperators():
    global OPERATORS
    global ACTION_TO_OP
    operators = OPERATORS
    operators.append(Operator("Rotate Up", lambda s: up(up(s))))
    operators.append(Operator("Rotate Down", lambda s: down(down(s))))
    operators.append(Operator("Rotate Left", lambda s: left(left(s))))
    operators.append(Operator("Rotate Right", lambda s: right(right(s))))
    operators.append(Operator("Rotate Front", lambda s: front(front(s))))
    operators.append(Operator("Rotate Back", lambda s: back(back(s))))
    ACTION_TO_OP["Up"] = operators[0]
    ACTION_TO_OP["Down"] = operators[1]
    ACTION_TO_OP["Left"] = operators[2]
    ACTION_TO_OP["Right"] = operators[3]
    ACTION_TO_OP["Front"] = operators[4]
    ACTION_TO_OP["Back"] = operators[5]


HEURISTICS = {'h_layer': h_layer, 'h_side': h_side}


# transition function
# the probability of making each move correctly is 100%
def T(s, a, sp):
    return 1

# reward function
def R(s, a, sp):
    if goalTest(sp):
        return 1000
    else:
        return -1

def displayOptimalPolicy(world):
    world.extractPolicy()
    for key, value in world.optPolicy.items():
        print(key, value)


def test():
    cube_MDP = MDP.MDP()
    cube_MDP.register_start_state(createInitialState())
    cube_MDP.register_actions(ACTIONS)
    cube_MDP.register_operators(OPERATORS)
    cube_MDP.register_transition_function(T)
    cube_MDP.register_reward_function(R)
    cube_MDP.register_describe_state(describeState)
    cube_MDP.register_goal_test(goalTest)
    cube_MDP.register_action_to_op(ACTION_TO_OP)
    cube_MDP.generateAllStates()
    cube_MDP.QLearning(0.8, 1000, 0.2)
    displayOptimalPolicy(cube_MDP)

#UNCOMMENT THE FOLLOWING LINE TO RUN Q-LEARNING
#test()
