import queue as Q
import importlib

COUNT = None
BACKLINKS = {}
BACKACTIONS = {}

print("\nWelcome to our A* Implementation for solving a Rubik's Cube")

# Ask the user which cube and heuristics they would like to use
# No error checking, assume user enters correct data
print("\nWhich Rubik's Cube would you like to solve: ")
print("\n[a] 2x2")
print("\n[b] 3x3")
rubik = input("\nEnter a or b: ").lower()
if rubik == 'a':
    Problem = importlib.import_module('rubik2x2')
else:
    Problem = importlib.import_module('rubik')
print("\nWhich Heuristic would you like to solve: ")
print("\n[a] Sides")
print("\n[b] Layers")
heuristicsInput = input("\nEnter a or b: ").lower()
if heuristicsInput == 'a':
    heuristics = Problem.HEURISTICS['h_side']
else:
    heuristics = Problem.HEURISTICS['h_layer']

# Function to run AStar
def runAStar():
    initial_state = Problem.createInitialState()
    print("This is your initial state:")
    Problem.describeState(initial_state)
    scramble = input("Would you like to scramble it? (y/n) ")
    while scramble is 'y':
        initial_state = Problem.scramble(initial_state)
        print("Your initial state is now:")
        Problem.describeState(initial_state)
        scramble = input("Would you like to scramble it again? (y/n) ")
    global COUNT, BACKLINKS, BACKACTIONS
    COUNT = 0
    IterativeAStar(initial_state)
    print()
    print("Solved with " + str(COUNT) + " states examined.")


def IterativeAStar(initial_state):
    global COUNT, BACKLINKS, BACKACTIONS
    OPEN = Q.PriorityQueue()
    OPEN.put((heuristics(initial_state), initial_state))
    LIST = []
    LIST.append(initial_state)
    CLOSED = []
    BACKLINKS[Problem.hashCode(initial_state)] = -1
    BACKACTIONS[Problem.hashCode(initial_state)] = 'Start State'
    while LIST != []:
        S_tuple = OPEN.get()
        S = S_tuple[1]
        step = S_tuple[0] - heuristics(S)
        LIST.remove(S)
        CLOSED.append(S)
        if Problem.goalTest(S):
            Problem.goalMessage()
            Problem.describeState(S)
            print("COUNT = " + str(COUNT))
            print("len(OPEN)=" + str(len(LIST)))
            print("len(CLOSED)=" + str(len(CLOSED)))
            backtrace(S)
            return

        COUNT += 1
        if (COUNT % 32) == 0:
            print(".", end="")
            if (COUNT % 128) == 0:
                print()
                Problem.describeState(S)
                print("COUNT = " + str(COUNT))
                print("len(OPEN)=" + str(len(LIST)))
                print("len(CLOSED)=" + str(len(CLOSED)))
        L = []
        for op in Problem.OPERATORS:
            new_state = op.state_transf(S)
            if not occurs_in(new_state, CLOSED):
                L.append(new_state)
                BACKLINKS[Problem.hashCode(new_state)] = S
                BACKACTIONS[Problem.hashCode(new_state)] = op.name
        repeat = -1
        for i in range(len(L)):
            for j in range(len(LIST)):
                if Problem.deepEquals(L[i], LIST[j]):
                    repeat = i;
                    break
        if repeat != -1:
            del L[repeat]
        for s2 in L:
            OPEN.put((step + 1 + heuristics(s2), s2))
        LIST = LIST + L


def backtrace(S):
    global BACKLINKS, BACKACTIONS
    X = BACKACTIONS[Problem.hashCode(S)]
    path = []
    while not S == -1:
        tuple = (X,S)
        path.append(tuple)
        S = BACKLINKS[Problem.hashCode(S)]
        if S != -1:
            X = BACKACTIONS[Problem.hashCode(S)]
        else :
            X = 'Done!'
    path.reverse()
    print("\nSolution path: ")
    for s in path:
        print()
        print(s[0] + ':')
        print()
        Problem.describeState(s[1])

    return path


def occurs_in(s1, lst):
    for s2 in lst:
        if Problem.deepEquals(s1, s2): return True
    return False


if __name__ == '__main__':
    runAStar()
