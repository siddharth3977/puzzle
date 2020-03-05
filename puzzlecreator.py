# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 21:53:31 2020

@author: siddharth
"""

import time
import json
import copy
#300221003
#033020020
#druu
# a = 0: free, 1: block 2: pawn_1 3: pawn_2 4: pawn_3 5: pawn_4 6: Pawn_5 7: Pawn_6 8: pawn_6
visitedboard=set()
#matrixInitial = [[3,0,0],[2,2,1],[0,0,3]]
#matrixfinal =   [[0,3,3],[0,2,1],[0,2,0]]
sol = []
#matrixInitial = [[3, 0, 4, 0], [5, 0, 0, 0], [0, 2, 1, 0], [1, 1, 0, 2]]
#matrixfinal =  [[0, 2, 3, 0], [0, 0, 5, 2], [0, 4, 1, 0], [1, 1, 0, 0]]
pCount = 0
maxlimit=10
int2 = 0

def solve(maze, path, level, matrixFinal, size):
    global visitedboard,maxlimit,sol
   
    Found = True

    for i in range(0, size):
        for j in range(0,size):
            if ((maze[i][j]> 1) and ( maze[i][j] != matrixFinal[i][j])):
                Found = False
    if Found:
        if ( level == 0):
            return False
        else:
            if (path.__len__()< maxlimit):
                sol = path
                print(path)
                print("No of moves",path.__len__())
                #print(time.time()-a)
                maxlimit=path.__len__()
        return True
    else:
        level += 1
        if (level > maxlimit):  #  need not require more than 20 strokes overall
            return False
        # create 4 mazecopy
        mazeup = copy.deepcopy(maze)
        mazedown = copy.deepcopy(maze)
        mazeleft = copy.deepcopy(maze)
        mazeright = copy.deepcopy(maze)
        for stroke in range(0, 4):
            if (stroke == 0):  # upper stroke
                for i in range(1, size):
                    for j in range(0, size):
                        if (mazeup[i - 1][j] == 0):
                            if (mazeup[i][j] != 1):
                                mazeup[i - 1][j] = mazeup[i][j]
                                mazeup[i][j] = 0
                                # create the hash
                hashbit = 0
                hashvalueup = 0
                for i in range(0, size):
                    for j in range(0, size):
                        hashvalueup = hashvalueup + (mazeup[i][j] << hashbit * 3)
                        hashbit += 1
                len = visitedboard.__len__()
                visitedboard.add(hashvalueup)
                #if the hash is not in the set submit new solve
                if visitedboard.__len__() > len:
#
                    pathup = copy.deepcopy(path)
                    pathup.append("U")
#                    print pathup
                    solve(mazeup, pathup, level, matrixFinal, size)
                    visitedboard.remove(hashvalueup)


            elif (stroke == 1):  # down stroke
                for i in range(size - 2, -1, -1):
                    for j in range(0, size):
                        if (mazedown[i + 1][j] == 0):
                            if (mazedown[i][j] != 1):
                                mazedown[i + 1][j] = mazedown[i][j]
                                mazedown[i][j] = 0
                                # create the hash
                hashbit = 0
                hashvaluedown = 0
                for i in range(0, size):
                    for j in range(0, size):
                        hashvaluedown = hashvaluedown + (mazedown[i][j] << hashbit * 3)
                        hashbit += 1
                len = visitedboard.__len__()
                visitedboard.add(hashvaluedown)
                #if the hash is not in the set submit new solve
                if visitedboard.__len__() > len:
#                    print mazedown
#                    print "level " + str(level) +" - " + str(hashvaluedown)+ " added" + " Down"
#                    hashdown=True
                    pathdown = copy.deepcopy(path)
                    pathdown.append("D")
#                    print pathdown
                    solve(mazedown, pathdown, level, matrixFinal, size)
                    visitedboard.remove(hashvaluedown)
               

            elif (stroke == 2):  #left stroke
                for i in range(1,size):
                    for j in range(0, size):  # loop to create same column
                        if mazeleft[j][i-1] == 0:
                            if mazeleft[j][i] != 1:
                                mazeleft[j][i-1] = mazeleft[j][i]
                                mazeleft[j][i] = 0
                # create the hash
                hashbit = 0
                hashvalueleft = 0
                for i in range(0, size):
                    for j in range(0, size):
                        hashvalueleft = hashvalueleft + (mazeleft[i][j] << hashbit * 3)
                        hashbit += 1
                len = visitedboard.__len__()
                visitedboard.add(hashvalueleft)
                #if the hash is not in the set submit new solve
                if visitedboard.__len__() > len:
#                    print mazeleft
#                    print "level " + str(level) +" - " + str(hashvalueleft)+ " added" + " Left"
#                    hashleft=True
                    pathleft = copy.deepcopy(path)
                    pathleft.append("L")
#                    print pathleft
                    solve(mazeleft, pathleft, level, matrixFinal, size)
                    visitedboard.remove(hashvalueleft)
                
            elif (stroke == 3):
                for i in range(size-2,-1,-1):
                    for j in range(0, size):
                        if mazeright[j][i+1] == 0:
                            if mazeright[j][i] != 1:
                                mazeright[j][i+1] = mazeright[j][i]
                                mazeright[j][i] = 0
                # create the hash
                hashbit = 0
                hashvalueright = 0
                for i in range(0, size):
                    for j in range(0, size):
                        hashvalueright = hashvalueright + (mazeright[i][j] << hashbit * 3)
                        hashbit += 1
                len = visitedboard.__len__()
                visitedboard.add(hashvalueright)
                #if the hash is not in the set submit new solve
                if visitedboard.__len__() > len:
#                    print mazeright
#                    print "level " + str(level) +" - " + str(hashvalueright)+ " added" + " Right"
#                    hashright=True
                    
                    pathright = copy.deepcopy(path)
                    pathright.append("R")
#                    print pathright
                    solve(mazeright, pathright, level, matrixFinal, size)
                    visitedboard.remove(hashvalueright)

def createMaze(puzzle,dim):
    maze = []
    for row in range(dim):
        mazeRow = []
        for col in range(dim):
            index = (row*dim)+col
            mazeRow.append(int(puzzle[index]))
        maze.append(mazeRow)
    return maze

def createMazeString(maze,dim):
    a=""
    for row in range(dim):
        for col in range(dim):
            if maze[row][col]==100:
                maze[row][col] = 'h'
            a = a+str(maze[row][col])
    return a

def createMazeFinal(matrixInitial,dim,matrixFinal):
     for row in range(dim):
        for col in range(dim):
           if matrixInitial[row][col]==1 and matrixFinal[row][col]==0:
               matrixFinal[row][col]=1
     return matrixFinal
 
#a=time.time()
#solve(matrixInitial,[],0)
#print(sol)
def findBlockerPosition(init, final):
    blockerList = []
    for a in range(len(init)):
        if init[a]=='1' and final[a]=='1':
            blockerList.append(a)
    return blockerList

def findOpenPosition(init, final):
    openList = []
    for a in range(len(init)):
        if init[a]=='0' and final[a]=='0':
            openList.append(a)
    return openList

def swapOpenBlocker(blockerList, openList, initialState, finalState, data):
    a = initialState
    b = finalState
    for bpos in blockerList:
        for opos in openList:
            initMat = list(a)
            finMat = list(b)
            initMat[bpos] = '0'
            initMat[opos] = '1'
            finMat[bpos] = '0'
            finMat[opos] = '1'
            initString = "".join(initMat)
            finalString =  "".join(finMat)
            solveNewPuzzle(initString, finalString, data)
        
def solveNewPuzzle(initString, finalString, data):
    print("-------------")
    global sol, pCount, visitedboard, maxlimit
    maxlimit = 10
    visitedboard = set()
    sol = []
    dim = int(len(initString) ** 0.5)  
    print(initString)
    print(finalString)
    matrixInitial = createMaze(initString,dim)
    matrixFinal = createMaze(finalString,dim)
    size=len(matrixFinal)
    solve(matrixInitial,[],0,matrixFinal,size)
    print(sol)
    if len(sol) > 0:
        pCount = pCount + 1
        with open('newInt3.json', 'a+') as outfile:
            newData = data
            newData['initialState'] = initString
            newData['solution'] = "".join(sol)
            json.dump(newData, outfile)
            outfile.write('\n')
            
 

def readFile():  
    global sol, pCount, maxlimit
    with open('int3.json') as f:
        lines = f.readlines()
        for line in lines:
            print(line)
            sol = []
            maxlimit = 10
            data = json.loads(line)
            dim = int(len(data['initialState']) ** 0.5)  
            matrixInitial = createMaze(data['initialState'],dim)
            matrixFinal = createMaze(data['solvedState'],dim)
            matrixFinal = createMazeFinal(matrixInitial,dim,matrixFinal)
            size=len(matrixFinal)
            #print(data)
            #print(data['initialState'])
            solve(matrixInitial,[],0,matrixFinal,size)
            if(len(sol)==len(data['solution'])):
                init = data['initialState']
                final = createMazeString(matrixFinal,dim)
                print(init)
                print(final)
                print("---------------------")
                blockerList = findBlockerPosition(data['initialState'],createMazeString(matrixFinal,dim))
                openList = findOpenPosition(data['initialState'],createMazeString(matrixFinal,dim))
                print(blockerList)
                print(openList)
                if(len(blockerList)>0 and len(openList)>0):
                    swapOpenBlocker(blockerList, openList, init, final, data)
            if pCount > 500:        
                break

readFile()        