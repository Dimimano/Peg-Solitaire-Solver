''' 
The program solves Peg Solitaire problems using the Depth-First search and Best-First search algorithms, while adopting some elements from Backtracking algorithms such as recursion
and memory that stores previous board states, in order to 'backtrack' from them. These backtracking elements are part of the 4 solvers that were createdand are further expained below.
The boards are converted into numpy (2D) matrices in order to be processed. Problems are read from an input file, while the solution is written to an output file.
'''
import sys
import numpy as np
import time

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
This function represents a Depth-First search solution that recursively traverses through the (hypothetical) search tree unti a solution is found. Board states that were previously
visited are stored in a list called memory and the function backtracks when it encounters them. The function takes as input the current board (represented as a numpy array),
goes through each peg on the board and check which moves are possible (and in which direction). If any legal move is possible on the first peg encountered, the move is executed
and through recursion the function, is again applied on the Updated board.

Input:  [array] Int numpy matrix that represents the board's current state. 
        [path] List of strings that stores the moves that were made on the current board.
        [memory] List of integers that represent, in an efficient way, previously encountered board states.
        
Output: [path] The final list that contains the moves for the first solution found. 
'''
def depth_first_solver(array,path,memory):
    #List that stores each of the 4 possible move directions
    directions = ['up', 'down', 'left', 'right']
    #List of strings that stores the moves that were made on the current board.
    moves_list = path
    
    #Go through each peg on the board..
    for i in range(totalLines):
        for j in range(totalColumns):
            #If a peg is found..
            if array[i][j] == 1:
                flag = 0
                
                #Check each one of the 4 possible move directions..
                for direction in directions:
                    
                    #If a move is possible..
                    if hasPossibleMove(array,i,j,direction):
                        
                        #Make the move and store the new board in a numpy array and a string that contain the move that was made.
                        nextMoveArray = np.copy(array)
                        nextMoveArray,move = makeTheMove(nextMoveArray,i,j,direction)
                        
                        #Check if the current board is previously encountered..
                        if boardPreviouslySeen(memory,convertToStr(nextMoveArray)):
                            flag = 1
                            #If yes go to the next direction/peg.
                            break
                        
                        #If the current board is not previously encountered save it.  
                        if not flag:
                            memory.append(convertToStr(nextMoveArray))
                        
                        #If there are no boards saved, save the current one.        
                        if not memory:
                            memory.append(convertToStr(nextMoveArray))
                        
                        #If the board is previously encountered skip to next direction/peg.
                        if flag:
                            continue
                        
                        #Store the move that was made.
                        moves_list.append(move)
                        
                        #If the problem is not solved..
                        if not solutionFound(nextMoveArray):
                            #recursively apply the solver to the current board.
                            depth_first_solver(nextMoveArray,moves_list,memory)
                            
                        #If the problem is solved stop and return the path.
                        else:
                            global solution_flag
                            solution_flag = 1
                            path = moves_list
                        if solution_flag:
                            return 1
                        
                        #If the move did not solve the problem remove it from the path.
                        moves_list.pop(len(moves_list)-1)
 
'''
This function implements a Best-First search solution that recursively traverses through the (hypothetical) search tree unti a solution is found. Board states that were previously
visited are stored in a list called memory and the function backtracks when it encounters them. The heuristic function used essentialy uses 2 criteria in order to rate each possible
move at the current point of the search. The first criterion is the number of available moves in the resulting board and the second one, is the number of isolated pegs in the resulting board
after the move is applied. This rating is calculated for each 'child node' (each possible move) from the current node in the search tree that is examined.
The ratings are saved in a dictionary where the key is the rating and the values are lists of the corresponding rated moves (as strings). The dictionary is then sorted in descending
order and the highest rated moves are applied to the board. The function is recursively applied based on the moves ratings until a solution is found. If two moves have the same rating,
the one that was first found is the first one to be applied.

Input:  [array] Int numpy matrix that represents the board's current state. 
        [path] List of strings that stores the moves that were made on the current board.
        [memory] List of integers that represent, in an efficient way, previously encountered board states.
        
Output: [path] The final list that contains the moves for the first solution found. 
'''                       

def heuristic_solver_rating(array,path,memory):
    directions = ['up', 'down', 'left', 'right']
    moves_list = path
    
    #This dictionary saves the rating for each possible move at the current search point.
    search_dict = {}
    
    
    for i in range(totalLines):
        for j in range(totalColumns):
            flag = 0
            if array[i][j] == 1:
                for direction in directions:
                    #Find the first peg that has an available move in some direction..
                    if hasPossibleMove(array,i,j,direction):
                        #Make the move and save the resulting board..
                        nextMoveArray = np.copy(array)
                        nextMoveArray,move = makeTheMove(nextMoveArray,i,j,direction)
                        availableMovesCounter = 0
                        nonIsolated = 0
                        
                        #For each peg in the resulting board, if a move is possible in some direction rate it based on..
                        for x in range(totalLines):
                            for y in range(totalColumns):
                                if nextMoveArray[x][y] == 1:
                                    for direction_secondary in directions:
                                        #The amount of possible moves for each peg and..
                                        if hasPossibleMove(nextMoveArray,x,y,direction_secondary):
                                            availableMovesCounter += 1
                                    #The amount of isolated pegs.
                                    if isIsolated(nextMoveArray,x,y):
                                        nonIsolated += 1
                                        
                        #Sum the results of the 2 criteria in the rating variable..                
                        rating = nonIsolated + availableMovesCounter
                        #If the current key-rating already exists update its (list) value with the corresponding move.
                        #Moves with same rating are saved in the same list and the one first found is the first one to be applied.
                        if rating in search_dict:
                            search_dict[rating].append(str(i) + str(j) + direction)
                        #else, create a new key-rating with a list that contains the corresponding move as its value.
                        else:
                            search_dict[rating] = [str(i) + str(j) + direction]

    #Sort the dictionary in descending order based on the keys (ratings) since we want the moves with highest rating.
    search_dict_sorted = {k: v for k, v in sorted(search_dict.items(), key=lambda item: item[0], reverse=True)}
    
    #Traverse through the sorted dictionary..
    for key,value in search_dict_sorted.items():
        flag = 0

        #For each move (value) in the dictionary (starting from the highest rated)..
        for peg_move in value:
            #Make the move and the save the resulting board.
            nextMoveArray = np.copy(array) 
            nextMoveArray,move = makeTheMove(nextMoveArray,int(peg_move[0]),int(peg_move[1]),peg_move[2:])
            
            #Check if the board was previously encountered.
            if boardPreviouslySeen(memory,convertToStr(nextMoveArray)):
                flag = 1
                break
                
            if not flag:
                memory.append(convertToStr(nextMoveArray))
                    
            if not memory:
                memory.append(convertToStr(nextMoveArray))
            
            if flag:
                continue
            moves_list.append(move)
            
            if not solutionFound(nextMoveArray):
                heuristic_solver_rating(nextMoveArray,moves_list,memory)
            else:
                global solution_flag
                solution_flag = 1
                path = moves_list
            if solution_flag:
                return 1
            moves_list.pop(len(moves_list)-1)

'''
This function implements a Best-First search solution that recursively traverses through the (hypothetical) search tree unti a solution is found. Board states that were previously
visited are stored in a list called memory and the function backtracks when it encounters them. The heuristic function used essentialy uses 1 criterion in order to rate each possible
move at the current point of the search. The criterion is the Manhattan Distance of each peg on the board with every other peg. This distance is calculated for each 'child node' 
(the resulting board for each possible move) from the current node in the search tree that is examined. The distances are saved in a dictionary where the key is the total distance 
and the values are lists of the corresponding moves (as strings). The dictionary is then sorted in asceding order and moves that result to a board with the smallest possible total 
distance are applied to the board. The function is recursively applied until a solution is found. If two moves have the same total distance, the one that was first found 
is the first one to be applied.

Input:  [array] Int numpy matrix that represents the board's current state. 
        [path] List of strings that stores the moves that were made on the current board.
        [memory] List of integers that represent, in an efficient way, previously encountered board states.
        
Output: [path] The final list that contains the moves for the first solution found. 
'''
                        
def heuristic_solver_manhattan(array,path,memory):
    directions = ['up', 'down', 'left', 'right']
    moves_list = path
    search_dict = {}
    
    for i in range(totalLines):
        for j in range(totalColumns):
            if array[i][j] == 1:
                for direction in directions:
                    if hasPossibleMove(array,i,j,direction):
                        nextMoveArray = np.copy(array)
                        nextMoveArray,move = makeTheMove(nextMoveArray,i,j,direction)
                        total_distance = 0
                        for x in range(totalLines):
                            for y in range(totalColumns):
                                #Calculate the total distance for each peg on the resulting board..
                                if nextMoveArray[x][y] == 1:
                                    total_distance = manhattanDistance(nextMoveArray,x,y) + total_distance
                        #And accordingly save it in the dictionary.
                        if total_distance in search_dict:
                            search_dict[total_distance].append(str(i) + str(j) + direction)
                        else:
                            search_dict[total_distance] = [str(i) + str(j) + direction]
    
    #Sort the dictionary in asceding order based on the keys (distance) since we want to start applying moves that result to boards with the least total distance between the pegs.
    search_dict_sorted = {k: v for k, v in sorted(search_dict.items(), key=lambda item: item[0])}
    for key,value in search_dict_sorted.items():
        flag = 0
        
        for peg_move in value:
            nextMoveArray = np.copy(array)
            nextMoveArray,move = makeTheMove(nextMoveArray,int(peg_move[0]),int(peg_move[1]),peg_move[2:])
            
            #Check if the board was previously encountered.
            if boardPreviouslySeen(memory,convertToStr(nextMoveArray)):
                flag = 1
                break
                
            if not flag:
                memory.append(convertToStr(nextMoveArray))
                    
            if not memory:
                memory.append(convertToStr(nextMoveArray))
            
            if flag:
                continue
            moves_list.append(move)
            
            if not solutionFound(nextMoveArray):
                heuristic_solver_manhattan(nextMoveArray,moves_list,memory)
            else:
                global solution_flag
                solution_flag = 1
                path = moves_list
            if solution_flag:
                return 1
            moves_list.pop(len(moves_list)-1)
            
'''
This function implements a Best-First search solution that recursively traverses through the (hypothetical) search tree unti a solution is found. Board states that were previously
visited are stored in a list called memory and the function backtracks when it encounters them. The heuristic function used essentialy uses 1 criterion in order to rate each possible
move at the current point of the search. The criterion is the Total (Square) Area on the board that is covered by the pegs. The covered area is calculated for each 'child node' 
(the resulting board for each possible move) from the current node in the search tree that is examined. The values are saved in a dictionary where the key is the total area 
and the values are lists of the corresponding moves (as strings). The dictionary is then sorted in asceding order, and moves that result to a board with the smallest possible total
covered area are applied to the board. The function is recursively applied until a solution is found. If two moves have the same total area, 
the one that was first found is the first one to be applied.

Input:  [array] Int numpy matrix that represents the board's current state. 
        [path] List of strings that stores the moves that were made on the current board.
        [memory] List of integers that represent, in an efficient way, previously encountered board states.
        
Output: [path] The final list that contains the moves for the first solution found. 
'''
            
def heuristic_solver_area(array,path,memory):
    directions = ['up', 'down', 'left', 'right']
    moves_list = path
    search_dict = {}
    
    for i in range(totalLines):
        for j in range(totalColumns):
            if array[i][j] == 1:
                for direction in directions:
                    if hasPossibleMove(array,i,j,direction):
                        nextMoveArray = np.copy(array)
                        nextMoveArray,move = makeTheMove(nextMoveArray,i,j,direction)
                        #Calculate the total area covered by the pegs on the resulting board..
                        area = areaCovered(nextMoveArray)
                        #And accordingly save it in the dictionary.
                        if area in search_dict:
                            search_dict[area].append(str(i) + str(j) + direction)
                        else:
                            search_dict[area] = [str(i) + str(j) + direction]
    
    #Sort the dictionary in asceding order based on the keys (area) since we want to start applying moves that result to boards with the least total area covered by the pegs.                        
    search_dict_sorted = {k: v for k, v in sorted(search_dict.items(), key=lambda item: item[0])}
    for key,value in search_dict_sorted.items():
        flag = 0
        
        for peg_move in value:
            nextMoveArray = np.copy(array)
            nextMoveArray,move = makeTheMove(nextMoveArray,int(peg_move[0]),int(peg_move[1]),peg_move[2:])
            
            #Check if the board was previously encountered.
            if boardPreviouslySeen(memory,convertToStr(nextMoveArray)):
                flag = 1
                break
                
            if not flag:
                memory.append(convertToStr(nextMoveArray))
                    
            if not memory:
                memory.append(convertToStr(nextMoveArray))
            
            if flag:
                continue
            moves_list.append(move)
            if not solutionFound(nextMoveArray):
                heuristic_solver_area(nextMoveArray,moves_list,memory)
            else:
                global solution_flag
                solution_flag = 1
                path = moves_list
            if solution_flag:
                return 1
            moves_list.pop(len(moves_list)-1)
            
'''
This function is used in order to find out whether a given board was previously encountered. Using the function 'convertToStr' the numpy array is converted to a String and saved
into a list. This list is given as input to this function together with the converted array we need to check.

Input:  [str_list] List of strings which represent the boards previously encountered while searching. 
        [string] The current board we want to check after being converted into a string.
        
Output: 1--> if the board is previously encountered (if the string is in the list) 
        2--> if it is a new board. 
'''
                        
def boardPreviouslySeen(str_list,string):
    if string in str_list:
        return 1
    else:
        return 0  

'''
This function is used in order to efficiently store the Peg Solitaire boards in a list. Looping through each of the board's (numpy array) elements, a string is created which encodes
the whole array as a sequence of its elements. If the given element is zero it is not included since their position never change while solving a problem (they just fill the array).

Input:  [array] Numpy array that represents the current board we want to convert into a string.
  
Output: The string that encodes the given array. 
'''          

def convertToStr(array):
    number = ""
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if array[i][j] != 0:
                number = number + str(int(array[i][j]))
    return number

'''
This function is used by the heuristic_solver_area in order to calculate the Total Square Area the pegs cover on the current board. 

Input:  [array] Numpy array that represents the current board from which the Total Square Area that is covered by the pegs will be calculated.
  
Output: The Total Square Area that is covered by the pegs. 
'''  

def areaCovered(array):
    max_line,max_column = 0,0
    min_line,min_column = array.shape[0],array.shape[1]
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if array[i][j] == 1:
                if i>max_line:
                    max_line = i
                if i<min_line:
                    min_line = i 
                if j>max_column:
                    max_column = j
                if j<min_column:
                    min_column = j 
    return ((max_line-min_line)+1)*((max_column-min_column)+1)

'''
This function is used by the heuristic_solver_manhattan in order to calculate the Total Distance between the pegs on the current board. 

Input:  [array] Numpy array that represents the current board from which the Total Distance between the pegs will be calculated.
  
Output: The Total Distance between the pegs. 
'''  
            
def manhattanDistance(array,indexL,indexC):
    mD = 0
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if array[i][j] == 1:
                mD = abs(indexL-i) + abs(indexC-j) + mD
    return mD
 
'''
This function is used by the heuristic_solver_rating in order to find out whether a peg is isolated on the given board. A peg is isolated if there is not a peg in each of the 4 legal
directions a move can have (up,down,left,right).

Input:  [array] Numpy array that represents the current board.
        [indexL] Line coordinate of the current peg.
        [indexC] Column coordinate of the current peg.
        
Output: 1--> if the peg is isolated
        2--> if it is not
''' 
                
def isIsolated(array,indexL,indexC):
    neighbors = 0
    if indexL+1<array.shape[0]:
        if array[indexL+1][indexC] == 1:
            neighbors += 1
    if indexL-1>=0:
        if array[indexL-1][indexC] == 1:
            neighbors += 1
    if indexC+1<array.shape[1]:
        if array[indexL][indexC+1] == 1:
            neighbors += 1
    if indexC-1>=0:
        if array[indexL][indexC-1] == 1:
            neighbors += 1
    if neighbors>0:
        return 1
    else:
        return 0
    
'''
This function is used by the heuristic_solver_rating in order to find out whether a move is possible from a given peg to a given direction.

Input:  [array] Numpy array that represents the current board.
        [indexL] Line coordinate of the current peg.
        [indexC] Column coordinate of the current peg.
        [direction] Direction in which the existence of a possible move is checked.
        
Output: 1--> if the move is possible
        2--> if it is not
''' 

def hasPossibleMove(array,indexL,indexC,direction):
    if direction == 'up':
        if indexL-2 >= 0:
            if array[indexL-2][indexC] == 2 and array[indexL-1][indexC] == 1:
                return 1
    elif direction == 'down':
        if indexL+2 < array.shape[0]:
            if array[indexL+2][indexC] == 2 and array[indexL+1][indexC] == 1:
                return 1
    elif direction == 'right':
        if indexC+2 < array.shape[1]:
            if array[indexL][indexC+2] == 2 and array[indexL][indexC+1] == 1:
                return 1
    elif direction == 'left':
        if indexC-2 >= 0:
            if array[indexL][indexC-2] == 2 and array[indexL][indexC-1] == 1:
                return 1
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

def makeTheMove(array,indexL,indexC,direction):
    if direction == 'up':
        array[indexL-2][indexC] = 1
        array[indexL-1][indexC] = 2
        array[indexL][indexC] = 2
        move = str(indexL+1) + " " + str(indexC+1) + " " + str(indexL-1) + " " + str(indexC+1)
        return array,move
    elif direction == 'down':
        array[indexL+2][indexC] = 1
        array[indexL+1][indexC] = 2
        array[indexL][indexC] = 2
        move = str(indexL+1) + " " + str(indexC+1) + " " + str(indexL+3) + " " + str(indexC+1)
        return array,move
    elif direction == 'right':
        array[indexL][indexC+2] = 1
        array[indexL][indexC+1] = 2
        array[indexL][indexC] = 2
        move = str(indexL+1) + " " + str(indexC+1) + " " + str(indexL+1) + " " + str(indexC+3)
        return array,move
    elif direction == 'left':
        array[indexL][indexC-2] = 1
        array[indexL][indexC-1] = 2
        array[indexL][indexC] = 2
        move = str(indexL+1) + " " + str(indexC+1) + " " + str(indexL+1) + " " + str(indexC-1)
        return array,move
    

#Below is the program's main function.
   
#Start the timer in order to compare the different algorithm's and read the given arguments from the program's execution.
start = time.time()
algorithm = str(sys.argv[1])
inputFile = str(sys.argv[2])
outputFile = str(sys.argv[3])


#Read the file that contains the problem's starting board.
f = open(inputFile, "r")

flag = 1
lineIndex = 0
columnIndex = 0
solution_flag = 0
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

#Use the selected solver.
path = []
memory = []
if algorithm == 'depth':
    depth_first_solver(array,path,memory)
elif  algorithm == 'best':
    if len(sys.argv)<5:
        heuristic_solver_area(array,path,memory)
    elif str(sys.argv[4]) == 'manhattan':
        heuristic_solver_manhattan(array,path,memory)
    elif str(sys.argv[4]) == 'rating':
        heuristic_solver_rating(array,path,memory)
        
#Write the result in the file.
f = open(outputFile, "a")
for line in path:
    if line:
        f.write(str(line) + '\n')
f.close()
end = time.time()
print(end-start, "seconds")
