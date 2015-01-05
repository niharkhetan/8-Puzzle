'''
Created on Sept 16, 2014
File Name: nkhetan-hw2-uninformed.py
Usage: Select 1 for BFS Or 2 for DFS
Output: Path Cost and Path to Goal

Many Initial States are commented in __main__
    Uncomment each of them to test for probems of different difficulty
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
    for i in range(currentState[3]):
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
    

def generalSearch(queue, limit, numRuns, UnInformedSearchType):
    ''' Search Procedure to search items
    Takes in : 
    Queue: this is an array of nodes
    limit: a limit on number of nodes to test
    numRuns: count of number of times this function is called
    unInformedSearchType: Type of search BFS | DFS'''
    while limit!=0:
        if queue == []:
            return False
        elif testProcedure(queue[0]):
            pathToGoal=outputProcedure(numRuns, queue[0])
            effBranchfactor = calculateBranchingFactor(numRuns+1+len(queue), queue[0][3])       
            printBoard(pathToGoal, queue[0][3])
            print ("Path Cost                  ::: "+str(queue[0][3]))            
            print ("No Of nodes generated      ::: "+ str(numRuns+1+len(queue)))
            print ("Effective branching factor ::: "+ str(effBranchfactor))
            break;
        #elif limit == 0:
            #print "Limit reached"
        else:
            limit -= 1
            numRuns += 1
            queue = expandProcedure(queue[0], queue[1:len(queue)], UnInformedSearchType)
    if limit == 0:
        print("<::   LIMIT REACHED   ::>")


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
    
def expandProcedure(firstNode, restOfTheNodes, UnInformedSearchType):
    '''Expands the nodes along a set of rules:
    For BFS Queue with FIFO
    For DFS Queue with LIFO
    firstNode : Current Node which will be expanded
    restOFTheNodes : Other nodes in the Queue
    UnInformedSearchType : To differentiate between BFS|DFS'''
    currentNodeToExpand = firstNode[0]    
    if UnInformedSearchType == "BFS":
        if alreadyVisited(currentNodeToExpand) == False:
            for i in range(3):
                for j in range(3):
                    if currentNodeToExpand[i][j] == " ":
                        '''case 1: i,j+1'''
                        if (j+1)<3:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i][j+1]
                            copyOfCurrentNodeToExpand[i][j+1] = temp
                            restOfTheNodes.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, firstNode[2]+1))
                        '''case 2: i+1,j'''
                        if (i+1)<3:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i+1][j]
                            copyOfCurrentNodeToExpand[i+1][j] = temp
                            restOfTheNodes.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, firstNode[2]+1))
                        '''case 3: i-1,j'''
                        if (i-1)>=0:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i-1][j]
                            copyOfCurrentNodeToExpand[i-1][j] = temp
                            restOfTheNodes.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, firstNode[2]+1))
                        '''case 4: i,j-1'''
                        if (j-1)>=0:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i][j-1]
                            copyOfCurrentNodeToExpand[i][j-1] = temp
                            restOfTheNodes.append(makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, firstNode[2]+1))            
            visited.append(firstNode)               
            return restOfTheNodes
        else:
            return restOfTheNodes
    elif UnInformedSearchType == "DFS":
        if alreadyVisited(currentNodeToExpand) == False:
            for i in range(3):
                for j in range(3):
                    if currentNodeToExpand[i][j] == " ":
                        '''case 1: i,j+1'''
                        if (j+1)<3:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i][j+1]
                            copyOfCurrentNodeToExpand[i][j+1] = temp
                            restOfTheNodes.insert(0,makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, firstNode[2]+1))
                        '''case 1: i+1,j'''
                        if (i+1)<3:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i+1][j]
                            copyOfCurrentNodeToExpand[i+1][j] = temp
                            restOfTheNodes.insert(0,makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, firstNode[2]+1))
                        '''case 1: i-1,j'''
                        if (i-1)>=0:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i-1][j]
                            copyOfCurrentNodeToExpand[i-1][j] = temp
                            restOfTheNodes.insert(0,makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, firstNode[2]+1))
                        '''case 1: i,j-1'''
                        if (j-1)>=0:
                            copyOfCurrentNodeToExpand = makeCopyOfBoard(currentNodeToExpand)
                            temp = copyOfCurrentNodeToExpand[i][j]   
                            copyOfCurrentNodeToExpand[i][j] = copyOfCurrentNodeToExpand[i][j-1]
                            copyOfCurrentNodeToExpand[i][j-1] = temp
                            restOfTheNodes.insert(0,makeNode(copyOfCurrentNodeToExpand, currentNodeToExpand, firstNode[2]+1, firstNode[2]+1))
            visited.append(firstNode)    
            return restOfTheNodes           
        else:            
            return restOfTheNodes

'''----------------------------------------------------------------------------------------------------------------------'''

def testBFS(init, goal, limit):
    '''For BFS Search
    init: initial state
    goal: goal state which it has to achieve
    limit: the number of times after which it should stop searching'''
    makingInitNode = makeNode(init, [], 0, 0)   
    queue = []
    queue.append(makingInitNode)
    generalSearch(queue, limit, 0, "BFS")
    return
'''----------------------------------------------------------------------------------------------------------------------'''

def testDFS(init, goal, limit):
    '''For DFS Search
    init: initial state
    goal: goal state which it has to achieve
    limit: the number of times after which it should stop searching'''    
    makingInitNode = makeNode(init, [], 0, 0)
    queue = []
    queue.append(makingInitNode)
    generalSearch(queue, limit, 0, "DFS")
    return
'''----------------------------------------------------------------------------------------------------------------------'''

if __name__ == '__main__':
    visited = []
    goalState  = makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")
    
   
    '''EASIEST'''
    #initialState = makeState(1, 2, 3, 4, 5, "blank", 7, 8, 6)
    
    '''EASY'''
    #initialState = makeState(2, "blank", 3, 1, 5, 6, 4, 7, 8)
    #initialState = makeState(1, 2, 3, "blank", 4, 6, 7, 5, 8)
    #initialState = makeState(1, 2, 3, 4, 5, 6, 7, "blank", 8)
    #initialState = makeState(1, "blank", 3, 5, 2, 6, 4, 7, 8)
    #initialState = makeState(1, 2, 3, 4, 8, 5, 7, "blank", 6)
    
    
    '''MEDIUM'''
    #initialState = makeState(2, 8, 3, 1, "blank", 5, 4, 7, 6)
    '''Dfs Works for this'''
    initialState = makeState(1, 2, 3, 4, 5, 6, "blank", 7, 8)  
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
    #initialState = makeState(3, 8, 5, 1, 6, 7, 4, 2, "blank")
    chooseBFSOrDSF = input(":::>> Enter 1: for BFS    OR    Enter 2: for DFS :::> ")
    if chooseBFSOrDSF == 1: 
        startTime = time.time()
        testBFS(initialState, goalState, 10000)
        endTime = time.time()
        print ("Time taken   :: "+str(endTime-startTime))
    elif chooseBFSOrDSF == 2: 
        startTime = time.time()
        testDFS(initialState, goalState, 10000)
        endTime = time.time()
        print ("Time taken   :: "+str(endTime-startTime))
    else:
        print("You have entered Wrong Input")
    
