'''
Created on Sept 16, 2014
File Name: nkhetan-hw2-informed.py
Usage: Select 1 for HEURISTIC-1 Or 2 for HEURISTIC-2 Or 3 for A* SEARCH 
Output: Path Cost and Path to Goal

Many Initial States are commented in __main__
    Uncomment each of them to test for problems of different difficulty
@author: NiharKhetan
'''

import time
import math

def checkForBlank(numbers):
    '''It just checks for a blank and if present it returns an empty space or it converts interger to string
    string -> string'''
    if numbers == 'blank':
        return " "
    else:
        return str(numbers)
    
def printBoard(path, pathCost):
    '''It prints the Path Cost and arranges the board for the 8 puzzle and prints it
    list,number -> nothing'''  
    
    for i in range(len(path)):
        print (checkForBlank(path[i][0][0])+" | "+checkForBlank(path[i][0][1])+" | "+checkForBlank(path[i][0][2]))
        print (checkForBlank(path[i][1][0])+" | "+checkForBlank(path[i][1][1])+" | "+checkForBlank(path[i][1][2]))
        print (checkForBlank(path[i][2][0])+" | "+checkForBlank(path[i][2][1])+" | "+checkForBlank(path[i][2][2]))
        print ("------------------")
    return
    
def makeState(nw, n, ne, w, c, e, sw, s, se):
    '''Generates and returns a board state based on given arguments 
    nw | NorthWest element of the puzzle
    n | North element of the puzzle
    ne | NorthEast element of the puzzle 
    w | West element of the puzzle
    c | Center element of the puzzle
    e | East element of the puzzle
    sw | SouthWest element of the puzzle
    s | South element of the puzzle
    se | SouthWest element of the puzzle '''
    board = [[" "," "," "],
            [" "," "," "],
            [" "," "," "]]
    board[0][0] = checkForBlank(nw)
    board[0][1] = checkForBlank(n)
    board[0][2] = checkForBlank(ne)
    board[1][0] = checkForBlank(w)
    board[1][1] = checkForBlank(c)
    board[1][2] = checkForBlank(e)
    board[2][0] = checkForBlank(sw)
    board[2][1] = checkForBlank(s)
    board[2][2] = checkForBlank(se)   
    return board

def testProcedure(currentState):    
    '''Test Procedure to check if the goal is reached
    list->boolean''' 
    if currentState[0] == goalState:
        return True    
    return False

def findParent(parentState):
    '''for a given state parentState considering it to be child of some parent returns its parent node details
    state -> Parent(current state, parent state)'''
    for i in range(len(visited)):
        if parentState == visited[i][0]:
            return (visited[i][0],visited[i][1])
        
def outputProcedure(numRuns, currentState):
    '''It backtracks to find the solution path once goal is reached
    int, state -> pathToGoal'''
    pathToGoal = []    
    curState = currentState[0]
    parentState = currentState[1]    
    pathToGoal.insert(0,curState)
    newParent = parentState
    for i in range(currentState[2]):
        newCur, newParent = findParent(newParent)       
        pathToGoal.insert(0,newCur)        
    return pathToGoal

def makeNode(state, parent, depth, pathCost):
    ''' Makes a current node which is of the sort:
    state: Current state of the node
    parent: Parent node which generated this node
    depth: depth at which this node is found
    numRuns: Cost of the path from Initial Node to the Current State
    [[1,2,5,4,3,7,"blank",9,8,6],[1,2,5,4,3,7,"blank",9,8,6], 2 , 2  ] '''
    return [state, parent, depth, pathCost]

def calculateBranchingFactor(numberNodesVisited, depth):
    '''It calculates the effective branching factor for a Search Problem as N power (1/d) 
    where N is the number of nodes visited and d is the depth where the solution is found.
    number, number -> number'''
    x = 1/float(depth)
    return math.pow(numberNodesVisited, x)
    #return int(math.ceil(math.pow(numberNodesVisited, x)))

def generalSearch(queue, limit, numRuns, informedSearchType):
    ''' Search Procedure to search items
    Takes in : 
    Queue: this is an array of nodes
    limit: a limit on number of nodes to test
    numRuns: count of number of times this function is called
    unInformedSearchType: Type of search Heuristic1 | Heuristic2 | A* Search'''
    while limit!=0:
        if queue == []:
            return False
        elif testProcedure(queue[0]):
            pathToGoal=outputProcedure(numRuns, queue[0])
            effBranchfactor = calculateBranchingFactor(numRuns+1+len(queue), queue[0][2])  
            printBoard(pathToGoal, queue[0][2])
            print ("Path Cost                  ::: "+str(queue[0][2]))
            print ("No Of nodes generated      ::: "+ str(numRuns+1+len(queue)))
            print ("Effective branching factor ::: "+ str(effBranchfactor))
            break;   
        else:
            limit -= 1
            numRuns += 1
            queue = expandProcedure(queue[0], queue[1:len(queue)], informedSearchType)
    if limit == 0:
        print("<::   LIMIT REACHED   ::>")       
            
'''----------------------------------------------------------------------------------------------------------------------'''

def makeCopyOfBoard(board):
    '''Creates a copy of board in another object'''
    copy = [[" "," "," "],
           [" "," "," "],
           [" "," "," "]]
    for i in range(3):
        for j in range(3):
            copy[i][j] = board[i][j]
    return copy    

def alreadyVisited(Node):
    '''Checks if the node has already been visited
    Node -> Boolean'''
    visitedFlag = False
    for count in range(len(visited)):
        if Node in visited[count]:
            visitedFlag = True
            break                
    return visitedFlag
    
def expandProcedure(firstNode, restOfTheNodes, informedSearchType):
    '''Expands the nodes along a set of rules:
    Heuristic Function 1 is defined as Linear Distance
    Heuristic Function 2 is defined as Eucledian Distance
    A* Search is degines a f(n) = h(n) + g(n) where h(n) is Eucledian Distance and g(n) is cost to current state from initial state
    firstNode : Current Node which will be expanded
    restOFTheNodes : Other nodes in the Queue
    UnInformedSearchType : To differentiate between Heuristic 1 | Heuristic2 | A* Search'''
    currentNodeToExpand = firstNode[0]
    if informedSearchType == "h1":
        if alreadyVisited(currentNodeToExpand) == False:
            for i in range(3):
                for j in range(3):
                    if currentNodeToExpand[i][j] == " ":                       
                        if (j+1)<3:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i][j+1]
                            copyOfCurrentNodeToExpand[i][j+1] = temp
                            restOfTheNodes.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, calcLinearDistance(copyOfCurrentNodeToExpand)))
                        if (i+1)<3:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i+1][j]
                            copyOfCurrentNodeToExpand[i+1][j] = temp
                            restOfTheNodes.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, calcLinearDistance(copyOfCurrentNodeToExpand)))
                        if (i-1)>=0:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i-1][j]
                            copyOfCurrentNodeToExpand[i-1][j] = temp
                            restOfTheNodes.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, calcLinearDistance(copyOfCurrentNodeToExpand)))
                        if (j-1)>=0:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i][j-1]
                            copyOfCurrentNodeToExpand[i][j-1] = temp
                            restOfTheNodes.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, calcLinearDistance(copyOfCurrentNodeToExpand)))
            
            visited.append(firstNode)     
            return maintainPriorityQueue(restOfTheNodes)
        else:
            return maintainPriorityQueue(restOfTheNodes)
    elif informedSearchType == "h2":
        if alreadyVisited(currentNodeToExpand) == False:
            for i in range(3):
                for j in range(3):
                    if currentNodeToExpand[i][j] == " ":                        
                        if (j+1)<3:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i][j+1]
                            copyOfCurrentNodeToExpand[i][j+1] = temp
                            restOfTheNodes.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, calcEucledianDistance(copyOfCurrentNodeToExpand)))
                        if (i+1)<3:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i+1][j]
                            copyOfCurrentNodeToExpand[i+1][j] = temp
                            restOfTheNodes.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, calcEucledianDistance(copyOfCurrentNodeToExpand)))
                        if (i-1)>=0:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i-1][j]
                            copyOfCurrentNodeToExpand[i-1][j] = temp
                            restOfTheNodes.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, calcEucledianDistance(copyOfCurrentNodeToExpand)))
                        if (j-1)>=0:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i][j-1]
                            copyOfCurrentNodeToExpand[i][j-1] = temp
                            restOfTheNodes.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, calcEucledianDistance(copyOfCurrentNodeToExpand)))
            
            visited.append(firstNode)           
            return maintainPriorityQueue(restOfTheNodes)
        else:
            return maintainPriorityQueue(restOfTheNodes)
    elif informedSearchType == "astar":
        '''if current node is already visited it would be in rest of the nodes'''
        visited.append(firstNode)
        nodesForOptimalPath.append(firstNode)        
        for i in range(3):
            for j in range(3):
                if currentNodeToExpand[i][j] == " ":                                     
                    eachNeighbourNode = []
                    if (j+1)<3:
                        copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                        temp = copyOfCurrentNodeToExpand[i][j]   
                        copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i][j+1]
                        copyOfCurrentNodeToExpand[i][j+1] = temp                        
                        eachNeighbourNode.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, calcEucledianDistance(copyOfCurrentNodeToExpand)+firstNode[2]+1))
                    if (i+1)<3:
                        copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                        temp = copyOfCurrentNodeToExpand[i][j]   
                        copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i+1][j]
                        copyOfCurrentNodeToExpand[i+1][j] = temp                        
                        eachNeighbourNode.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, calcEucledianDistance(copyOfCurrentNodeToExpand)+firstNode[2]+1))
                    if (i-1)>=0:
                        copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                        temp = copyOfCurrentNodeToExpand[i][j]   
                        copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i-1][j]
                        copyOfCurrentNodeToExpand[i-1][j] = temp                       
                        eachNeighbourNode.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, calcEucledianDistance(copyOfCurrentNodeToExpand)+firstNode[2]+1))
                    if (j-1)>=0:
                        copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                        temp = copyOfCurrentNodeToExpand[i][j]   
                        copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i][j-1]
                        copyOfCurrentNodeToExpand[i][j-1] = temp                        
                        eachNeighbourNode.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, calcEucledianDistance(copyOfCurrentNodeToExpand)+firstNode[2]+1))
        for i in range(len(eachNeighbourNode)):
            if eachNeighbourNode[i] in nodesForOptimalPath: 
                indexOfNode = nodesForOptimalPath.index(eachNeighbourNode[i])
                if eachNeighbourNode[i][3] < nodesForOptimalPath[indexOfNode][3]:                    
                    for j in range(len(nodesForOptimalPath)):                    
                        if eachNeighbourNode[i][1] == nodesForOptimalPath[j][0]:
                            del nodesForOptimalPath[j]
                            break
                    restOfTheNodes.append(eachNeighbourNode[i])                    
                
            elif eachNeighbourNode[i] in restOfTheNodes:
                indexOfNode = restOfTheNodes.index(eachNeighbourNode[i])
                if eachNeighbourNode[i][3] < restOfTheNodes[indexOfNode][3]:                    
                    restOfTheNodes[indexOfNode][3] = eachNeighbourNode[i][3]
            else:
                restOfTheNodes.append(eachNeighbourNode[i])  
        return maintainPriorityQueue(restOfTheNodes)
                    


def maintainPriorityQueue(queue):
    '''it keeps the Priority Queue sorted in ascending order so that node iwth highest priority (lowest cost) is always expanded first'''
    for j in xrange(len(queue)-1):
        minEle = j
        for i in xrange(j+1, len(queue)):
            if(queue[i][3]<queue[minEle][3]):
                minEle = i
        
        if(minEle != j):
            temp = queue[j]
            queue[j] = queue[minEle]
            queue[minEle] = temp
    return queue                  
    

def calcLinearDistance(initialState):
    '''It calculates Linear Distance for 8 Puzzle
    for an initialState linear distance is the sum of number of tiles which are not at their position that is they have to be moved
    so Heuristic Function 1 is based on Linear Distance
    initialState -> pathCost'''
    pathCost = 0
    for i in range(3):
        for j in range(3):
            if(initialState[i][j] != goalState[i][j] != " "):
                pathCost+=1
    return pathCost


def testInformedSearch1(init, goal, limit):
    '''For Heuristic Function 1
    init: initial state
    goal: goal state which it has to achieve
    limit: the number of times after which it should stop searching'''
    makingInitNode = makeNode(init, [], 0, calcLinearDistance(init))
    queue = []
    queue.append(makingInitNode)  
    generalSearch(queue, limit, 0, 'h1')   
    pass

def getPositionInGoalState(valueOfElement):
    '''It returns the position of a particular number which is in initial state, in Goal state
    number -> (number,number)'''
    for i in range(3):
        for j in range(3):
            if valueOfElement == goalState[i][j]:
                return (i,j)

def calcEucledianDistance(initialState):
    '''It calculates Euclidean Distance for 8 Puzzle
    for an initialState Euclidean distance is the sum of moves for each number in initial state, to move it to the respective goal state
    so Heuristic Function 2 is based on Euclidean Distance
    initialState -> pathCost'''
    pathCost = 0
    for i in range(3):
        for j in range(3):
            if initialState[i][j] != " ":
                if initialState[i][j] != goalState[i][j]:
                    x,y = getPositionInGoalState(initialState[i][j])
                    pathCost = pathCost + (abs(x-i)+abs(y-j))
    return pathCost

def testInformedSearch2(init, goal, limit):
    '''For Heuristic Function 2
    init: initial state
    goal: goal state which it has to achieve
    limit: the number of times after which it should stop searching'''    
    makingInitNode = makeNode(init, [], 0, calcEucledianDistance(init))
    queue = []
    queue.append(makingInitNode)
    generalSearch(queue, limit, 0, 'h2')   
    pass

def testAStar(init, goal, limit):
    '''For A* Search
    init: initial state
    goal: goal state which it has to achieve
    limit: the number of times after which it should stop searching'''
    makingInitNode = makeNode(init, [], 0, calcEucledianDistance(init)+0)
    queue = []
    queue.append(makingInitNode)
    generalSearch(queue, limit, 0, 'astar')

if __name__ == '__main__':
    visited = []
    nodesForOptimalPath = []
    goalState  = makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")
    
    '''EASY'''
    #initialState = makeState(2, "blank", 3, 1, 5, 6, 4, 7, 8)
    #initialState = makeState(1, 2, 3, "blank", 4, 6, 7, 5, 8)
    #initialState = makeState(1, 2, 3, 4, 5, 6, 7, "blank", 8)
    #initialState = makeState(1, "blank", 3, 5, 2, 6, 4, 7, 8)
    #initialState = makeState(1, 2, 3, 4, 8, 5, 7, "blank", 6)
    
    '''MEDIUM'''
    #initialState = makeState(2, 8, 3, 1, "blank", 5, 4, 7, 6)
    #initialState = makeState(1, 2, 3, 4, 5, 6, "blank", 7, 8)
    #initialState = makeState("blank", 2, 3, 1, 5, 6, 4, 7, 8)
    #initialState = makeState(1, 3, "blank", 4, 2, 6, 7, 5, 8)
    #initialState = makeState(1, 3, "blank", 4, 2, 5, 7, 8, 6)
    
    '''HARD'''
    #initialState = makeState("blank", 5, 3, 2, 1, 6, 4, 7, 8)
    #initialState = makeState(5, 1, 3, 2, "blank", 6, 4, 7, 8)
    #initialState = makeState(2, 3, 8, 1, 6, 5, 4, 7, "blank")
    #initialState = makeState(1, 2, 3, 5, "blank", 6, 4, 7, 8)
    #initialState = makeState("blank", 3, 6, 2, 1, 5, 4, 7, 8)
    
    '''HARDEST'''
    #initialState = makeState(2, 6, 5, 4, "blank", 3, 7, 1, 8)
    #initialState = makeState(3, 6, "blank", 5, 7, 8, 2, 1, 4)
    #initialState = makeState(1, 5, "blank", 2, 3, 8, 4, 6, 7)
    #initialState = makeState(2, 5, 3, 4, "blank", 8, 6, 1, 7)
    initialState = makeState(3, 8, 5, 1, 6, 7, 4, 2, "blank")
    
    chooseSearchMethod = input(":::>> Enter 1: for Heuristic 1    OR    Enter 2: for Heuristic 2    OR    Enter 3: for A* Search  :::> ")
    if chooseSearchMethod == 1:
        startTime = time.time() 
        testInformedSearch1(initialState, goalState, 10000)
        endTime = time.time()
        print ("Time taken   :: "+str(endTime-startTime))
    elif chooseSearchMethod == 2:
        startTime = time.time() 
        testInformedSearch2(initialState, goalState, 10000)
        endTime = time.time()
        print ("Time taken   :: "+str(endTime-startTime))
    elif chooseSearchMethod == 3:
        startTime = time.time()
        testAStar(initialState, goalState, 10000)
        endTime = time.time()
        print ("Time taken   :: "+str(endTime-startTime))
    else:
        print("You have entered Wrong Input")
