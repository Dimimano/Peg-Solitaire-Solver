''' 
This program is created in order to verify the solutions created by the PegSolitaireSolver.py. It takes as input the original
problem which it translates into a numpy array, as well as the moves that define the solution which it applies one-by-one to
the numpy array. If there is only one '1' in the array the program prints positive answer.
'''

import sys
import numpy as np

'''
This function checks whether the problem is solved by counting if there is only one peg on the board.

Input: [array] Int numpy matrix that represents the board's current state.
Output: 1--> if there is only 1 peg on the board 
        2--> in every other case.
'''

def solutionFound(array):
    if np.count_nonzero(array == 1) == 1:
        return 1
    else:
        return 0

'''
This function is used from all the solvers in oder to create apply a given move to the current board and create the next one.

Input:  [array] Numpy array that represents the current board.
        [indexL] Line coordinate of the current peg.
        [indexC] Column coordinate of the current peg.
        [direction] Direction in which the existence of a possible move is checked.
        
Output: [array] The updated array after the given move was applied.
        [move] A string that contains the move that was made to the array.
''' 
   
def makeTheMove(array, n1, n2, n3, n4):
    start_line_index = int(n1) - 1
    start_column_index = int(n2) - 1
    end_line_index = int(n3) - 1
    end_column_index = int(n4) - 1
    empty = []
    
    if start_line_index == end_line_index:
        if start_column_index > end_column_index:
            median = start_column_index-1
        else:
            median = end_column_index-1
        if array[start_line_index][median] != 1:
            return 0,empty
        else:
            array[start_line_index][start_column_index] = 2
            array[start_line_index][median] = 2
            array[end_line_index][end_column_index] = 1
            return 1,array
        
    elif start_column_index == end_column_index:
        if start_line_index > end_line_index:
            median = start_line_index-1
        else:
            median = end_line_index-1
        if array[median][start_column_index] != 1:
            return 0,empty
        else:
            array[start_line_index][start_column_index] = 2
            array[median][start_column_index] = 2
            array[end_line_index][end_column_index] = 1
            return 1,array
            
    else:
        return 0,empty
            

inputFile = str(sys.argv[1])
outputFile = str(sys.argv[2])

f = open(inputFile, "r")

flag = 1
lineIndex = 0
columnIndex = 0
for line in f:
    if len(line) == 4 and flag:
        totalLines = int(line[0])
        totalColumns = int(line[2])
        array = np.zeros((totalLines, totalColumns))
        flag = 0
    else:
        for element in line:
            if element == '\n' or element == ' ':
                continue
            array[lineIndex][columnIndex] = int(element)
            columnIndex += 1
        lineIndex += 1
        columnIndex = 0

f.close()
f = open(outputFile, "r")

for line in f:
    line_no_spaces = line.replace(' ','')
    move = list(line_no_spaces)
    makeTheMove(array,move[0],move[1],move[2],move[3])

if solutionFound(array):
    print("The solution is valid.")    
else:
    print("The solution is not valid.")
        

