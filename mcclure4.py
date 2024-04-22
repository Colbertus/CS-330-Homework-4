# Colby McClure CS 330 Homework 4
# Date: 4/26/34
# Description: This program is a state-machine implementation of the r code given

#**********************************************************************************************************************************#
'''
Architecture statement: If you already know the functionality of the R code then there is no need to read this, this program 
closely follows the design of the R code given. The program is split into two scenarios, the first scenario is a trace scenario
while the second scenario is primarily used to get the final results after a big number of iterations. Each function for each 
state behaves the same as the R code given. All it does is append the state to the output file and increment the state counter for
that respective state. For each iteration, the state machine starts at 'Follow' and will continue to run until the state is 'Done'.
The state machine will randomly choose a number between 0 and 1 and depending on the state, it will transition to the next state
based on the probabilities given. The state machine will continue to run until the state is 'Done'. After the state machine has
finished running, the state and transition frequencies are calculated and outputted to the output file. The output file will contain
the scenario, trace, iterations, transition probabilities, state counts, state frequencies, transition counts, and transition 
frequencies. The only difference between one output to another is that the first scenario will have the trace of each iteration
while the second scenario will not have the trace of each iteration. But while the state machine runs, it will call each respective
function for each state and append the state to the output file until the state is 'Done' for that particular iteration.
'''
#**********************************************************************************************************************************#

# Needed Imports 
import random
import numpy as np

# Initialize the scenario
# NOTE: Change the scenario to 1 or 2 to run the respective scenario
scenario = 2

# Initialize the output file for both scenarios
output = ['output.txt', 'output2.txt'][scenario - 1]

# Initialize the trace scenario for both scenarios 
scenarioTrace = [True, False][scenario - 1]

# Initialize the probabilities for each state for each scenario
transition_probability = [[0.8, 0.4, 0.3, 0.4, 0.3, 0.3, 0.8, 0.8, 0.8],
                         [0.9, 0.6, 0.3, 0.2, 0.2, 0.4, 0.7, 0.9, 0.7]][scenario - 1]

# Initialize the sequence of states for each scenario
stateSequence = [[i for i in range(1, 8)], [7] + [i for i in range(1, 7)]][scenario - 1]

# Initialize the sequence of transitions for each scenario
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

#***********************************************************************#

# Action functions for each state which won't fully execute unless the scenario is 1

# Follow Action Function
def followAction(): 
    stateCount[Follow] += 1
    if scenario == 1:
        with open(output, 'a') as f:
            f.write('state = 1 Follow\n')

# Pull Out Action Function
def pullOutAction():
    stateCount[Pull_Out] += 1
    if scenario == 1:
        with open(output, 'a') as f:
            f.write('state = 2 Pull Out\n')

# Accelerate Action Function
def accelerateAction():
    stateCount[Accelerate] += 1
    if scenario == 1:
        with open(output, 'a') as f:
            f.write('state = 3 Accelerate\n')

# Pull In Ahead Action Function
def pullInAheadAction():
    stateCount[Pull_In_Ahead] += 1
    if scenario == 1:
        with open(output, 'a') as f:
            f.write('state = 4 Pull In Ahead\n')

# Pull In Behind Action Function    
def pullInBehindAction():
    stateCount[Pull_In_Behind] += 1
    if scenario == 1:
        with open(output, 'a') as f:
            f.write('state = 5 Pull In Behind\n')

# Decelerate Action Function
def decelerateAction():
    stateCount[Decelerate] += 1
    if scenario == 1:
        with open(output, 'a') as f:
            f.write('state = 6 Decelerate\n')

# Done Action Function
def doneAction():
    stateCount[Done] += 1
    if scenario == 1: 
        with open(output, 'a') as f:
            f.write('state = 7 Done\n')

#***********************************************************************#

# Initialize the number of iterations for each scenario
iterations = [100, 1000000][scenario - 1]

# For each iteration, run the state machine
for i in range(iterations):

    # Don't append the iteration number unless it is scenario 1
    if scenario == 1:
        with open(output, 'a') as f:
            f.write('\nIteration = ' + str(i) + '\n')
    
    # Starting our state machine at Follow
    state = 0
    followAction() 

    # While the state is not 'Done', do the following 
    while state != Done: 
        
        # Randomly choose a number between 0 and 1
        r = random.uniform(0.0, 1.0) 

        # If the state is follow then pull out or stay in follow depending on the random number 
        if state == Follow:
            if r < transition_probability[0]:
                pullOutAction()
                transitionCount[0] += 1
                state = Pull_Out
            else:
                state = Follow
                followAction()
        
        # If the state is pull out then accelerate, pull in behind, or stay in pull out depending on the random number 
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
        
        # If the state is accelerate then pull in ahead, pull in behind, decelerate, or stay in accelerate depending on the random number
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
        
        # If the state is pull in ahead then go to done or stay in pull in ahead depending on the random number
        elif state == Pull_In_Ahead:
            if r < transition_probability[8]:
                doneAction()
                transitionCount[8] += 1
                state = Done
            else:
                state = Pull_In_Ahead
                pullInAheadAction()

        # If the state is pull in behind then follow or stay in pull in behind depending on the random number
        elif state == Pull_In_Behind:
            if r < transition_probability[6]:
                followAction()
                transitionCount[6] += 1
                state = Follow
            else:
                state = Pull_In_Behind
                pullInBehindAction()
        
        # If the state is decelerate then pull in behind or stay in decelerate depending on the random number
        elif state == Decelerate:
            if r < transition_probability[7]:
                pullInBehindAction()
                transitionCount[7] += 1
                state = Pull_In_Behind
            else:
                state = Decelerate
                decelerateAction()
        
        # If the state is done then stay in done
        else:
            state = 6
            doneAction()

            with open(output, 'a') as f:
                f.write('\n')

#***********************************************************************#
 
with open(output, 'a') as f:
    f.write('\n')

# Calculate the state and transition frequencies
stateFrequency = np.array(stateCount) / sum(stateCount)
stateFrequency = [stateFrequency[i - 1] for i in stateSequence]

transitionFrequency = np.array(transitionCount) / sum(transitionCount)
transitionFrequency = [transitionFrequency[i - 1] for i in transitionSequence]

# Output the final results to the output file 
with open(output, 'a') as f:
    f.write('Scenario = ' + str(scenario) + '\n')
    f.write('Trace = ' + str(scenarioTrace) + '\n')
    f.write('Iterations = ' + str(iterations) + '\n')
    f.write('Transition Probabilities = ' + ' '.join(map(str, transition_probability)) + '\n')
    f.write('State Counts = ' + ' '.join(map(str, stateCount)) + '\n')
    f.write('State Frequencies = ' + ' '.join(map(str, stateFrequency)) + '\n')
    f.write('Transition Counts = ' + ' '.join(map(str, transitionCount)) + '\n')
    f.write('Transition Frequencies = ' + ' '.join(map(str, transitionFrequency)) + '\n')

