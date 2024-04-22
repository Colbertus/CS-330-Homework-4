# Colby McClure CS 330 Homework 4
# Date: 4/26/34

# Needed Imports 
import random
import numpy as np

# Initialize the scenario
scenario = 2

# Initialize the output file
output = ['output.txt', 'output2.txt'][scenario - 1]

# Initialize the trace scenario
scenarioTrace = [True, False][scenario - 1]

# Initialize the probabilities for each state
transition_probability = [[0.8, 0.4, 0.3, 0.4, 0.3, 0.3, 0.8, 0.8, 0.8],
                         [0.9, 0.6, 0.3, 0.2, 0.2, 0.4, 0.7, 0.9, 0.7]][scenario - 1]

# Initialize the sequence of states
stateSequence = [[i for i in range(1, 8)], [7] + [i for i in range(1, 7)]][scenario - 1]

# Initialize the sequence of transitions
transitionSequence = [[i for i in range(1, 9)], [9] + [i for i in range(1, 9)]][scenario - 1]

# Constants used for each state
Follow = 0
Pull_Out = 1
Accelerate = 2
Pull_In_Ahead = 3
Pull_In_Behind = 4
Decelerate = 5
Done = 6

# Initialize the counters for the states and transitions
stateCount = [0 for _ in range(7)] 
transitionCount = [0 for _ in range(9)]

def followAction(): 
    stateCount[Follow] += 1
    if scenario == 1:
        with open(output, 'a') as f:
            f.write('state = 1 Follow\n')

def pullOutAction():
    stateCount[Pull_Out] += 1
    if scenario == 1:
        with open(output, 'a') as f:
            f.write('state = 2 Pull Out\n')

def accelerateAction():
    stateCount[Accelerate] += 1
    if scenario == 1:
        with open(output, 'a') as f:
            f.write('state = 3 Accelerate\n')

def pullInAheadAction():
    stateCount[Pull_In_Ahead] += 1
    if scenario == 1:
        with open(output, 'a') as f:
            f.write('state = 4 Pull In Ahead\n')
    
def pullInBehindAction():
    stateCount[Pull_In_Behind] += 1
    if scenario == 1:
        with open(output, 'a') as f:
            f.write('state = 5 Pull In Behind\n')

def decelerateAction():
    stateCount[Decelerate] += 1
    if scenario == 1:
        with open(output, 'a') as f:
            f.write('state = 6 Decelerate\n')

def doneAction():
    stateCount[Done] += 1
    if scenario == 1: 
        with open(output, 'a') as f:
            f.write('state = 7 Done\n')

iterations = [100, 1000000][scenario - 1]

for i in range(iterations):

    if scenario == 1:
        with open(output, 'a') as f:
            f.write('\nIteration = ' + str(i) + '\n')
    
    state = 0
    
    followAction() 

    while state != Done: 
        
        r = random.uniform(0.0, 1.0) 

        if state == Follow:
            if r < transition_probability[0]:
                pullOutAction()
                transitionCount[0] += 1
                state = Pull_Out
            else:
                state = Follow
                followAction()
        
        elif state == Pull_Out:
            if r < transition_probability[1]:
                accelerateAction()
                transitionCount[1] += 1
                state = Accelerate
            elif r < sum(transition_probability[1:4:2]):
                transitionCount[3] += 1
                state = Pull_In_Behind
                pullInBehindAction()
            else:
                state = Pull_Out
                pullOutAction()
        
        elif state == Accelerate:
            if r < transition_probability[2]:
                pullInAheadAction()
                transitionCount[2] += 1
                state = Pull_In_Ahead
            elif r < sum(transition_probability[2:5:2]):
                transitionCount[4] += 1
                state = Pull_In_Behind
                pullInBehindAction()
            elif r < sum(transition_probability[i] for i in [2, 4, 5]):
                transitionCount[5] += 1
                state = Decelerate
                decelerateAction()
            else:
                state = Accelerate
                accelerateAction()
        
        elif state == Pull_In_Ahead:
            if r < transition_probability[8]:
                doneAction()
                transitionCount[8] += 1
                state = Done
            else:
                state = Pull_In_Ahead
                pullInAheadAction()

        elif state == Pull_In_Behind:
            if r < transition_probability[6]:
                followAction()
                transitionCount[6] += 1
                state = Follow
            else:
                state = Pull_In_Behind
                pullInBehindAction()
        
        elif state == Decelerate:
            if r < transition_probability[7]:
                pullInBehindAction()
                transitionCount[7] += 1
                state = Pull_In_Behind
            else:
                state = Decelerate
                decelerateAction()
        
        else:
            state = 6
            doneAction()

            with open(output, 'a') as f:
                f.write('\n')
 

with open(output, 'a') as f:
    f.write('\n')

stateFrequency = np.array(stateCount) / sum(stateCount)
stateFrequency = [stateFrequency[i - 1] for i in stateSequence]

transitionFrequency = np.array(transitionCount) / sum(transitionCount)
transitionFrequency = [transitionFrequency[i - 1] for i in transitionSequence]

with open(output, 'a') as f:
    f.write('Scenario = ' + str(scenario) + '\n')
    f.write('Trace = ' + str(scenarioTrace) + '\n')
    f.write('Iterations = ' + str(iterations) + '\n')
    f.write('Transition Probabilities = ' + ' '.join(map(str, transition_probability)) + '\n')
    f.write('State Counts = ' + ' '.join(map(str, stateCount)) + '\n')
    f.write('State Frequencies = ' + ' '.join(map(str, stateFrequency)) + '\n')
    f.write('Transition Counts = ' + ' '.join(map(str, transitionCount)) + '\n')
    f.write('Transition Frequencies = ' + ' '.join(map(str, transitionFrequency)) + '\n')



