 # -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 12:41:30 2019

@author: siddharth
"""

import copy


import sqlite3 as lite

blockerPuzzle = []
mazPuzzles = 10
problemCreatedCounter = {3:20,4:20,5:0,6:0,7:20}
confull = lite.connect('DB_GameData.db')
curfull= confull.cursor()
curfull.execute('select * from puzzles')
data = curfull.fetchall()

# a = 0: free, 1: block 2: pawn_1 3: pawn_2 4: pawn_3 5: pawn_4 6: Pawn_5 7: Pawn_6 8: pawn_6
visitedboard=set()

maxlimit=8
#f= open("puzzles.txt","w+")

def solve(maze, path, level, matrixfinal):
    size=len(matrixfinal)
    global visitedboard,maxlimit
   
    Found = True

    for i in range(0, size):
        for j in range(0,size):
            if ((maze[i][j]> 1) and ( maze[i][j] != matrixfinal[i][j])):
                Found = False
    if Found:
        if ( level == 0):
            return False,[]
        else:
            if (path.__len__()< maxlimit):
                #print(path)
                #print("No of moves",path.__len__())
                maxlimit=path.__len__()
                return True,path
        return False,[]
    else:
        level += 1
        if (level > maxlimit):  #  need not require more than 20 strokes overall
            return False,path
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
                            if (mazeup[i][j] != 1 and mazeup[i][j] != 100):
                                mazeup[i - 1][j] = mazeup[i][j]
                                mazeup[i][j] = 0
                        if (mazeup[i-1][j] == 100):
                            if(mazeup[i][j] != 1 and mazeup[i][j] != 0):
                                mazeup[i-1][j] = 0
                                mazeup[i][j] = 0
                            
                                # create the hash
                hashbit = 0
                hashvalueup = 0
                for i in range(0, size):
                    for j in range(0, size):
                        hashvalueup = hashvalueup + (mazeup[i][j] << hashbit * 3)
                        hashbit += 1
                len1 = visitedboard.__len__()
                visitedboard.add(hashvalueup)
                #if the hash is not in the set submit new solve
                if visitedboard.__len__() > len1:
#
                    pathup = copy.deepcopy(path)
                    pathup.append("U")
#                    print pathup
                    ans,sol = solve(mazeup, pathup, level,matrixfinal)
                    visitedboard.remove(hashvalueup)
                    if ans==True:
                        return True,sol

            elif (stroke == 1):  # down stroke
                for i in range(size - 2, -1, -1):
                    for j in range(0, size):
                        if (mazedown[i + 1][j] == 0):
                            if (mazedown[i][j] != 1 and mazedown[i][j] !=100):
                                mazedown[i + 1][j] = mazedown[i][j]
                                mazedown[i][j] = 0
                        if (mazedown[i+1][j] == 100):
                            if(mazedown[i][j] != 1 and mazedown[i][j] != 0):
                                mazedown[i+1][j] = 0
                                mazedown[i][j] = 0        
                                # create the hash
                                
                hashbit = 0
                hashvaluedown = 0
                for i in range(0, size):
                    for j in range(0, size):
                        hashvaluedown = hashvaluedown + (mazedown[i][j] << hashbit * 3)
                        hashbit += 1
                len1 = visitedboard.__len__()
                visitedboard.add(hashvaluedown)
                #if the hash is not in the set submit new solve
                if visitedboard.__len__() > len1:
#                    print mazedown
#                    print "level " + str(level) +" - " + str(hashvaluedown)+ " added" + " Down"
#                    hashdown=True
                    pathdown = copy.deepcopy(path)
                    pathdown.append("D")
#                    print pathdown
                    ans,sol=solve(mazedown, pathdown, level,matrixfinal)
                    visitedboard.remove(hashvaluedown)
                    if ans==True:
                        return True,sol
               

            elif (stroke == 2):  #left stroke
                for i in range(1,size):
                    for j in range(0, size):  # loop to create same column
                        if mazeleft[j][i-1] == 0:
                            if (mazeleft[j][i] != 1 and mazeleft[j][i]!=100):
                                mazeleft[j][i-1] = mazeleft[j][i]
                                mazeleft[j][i] = 0
                        if (mazeleft[j][i-1] == 100):
                            if(mazeleft[j][i] != 1 and mazeleft[j][i] != 0):
                                mazeleft[j][i-1] = 0
                                mazeleft[j][i] = 0            
                                
                # create the hash
                hashbit = 0
                hashvalueleft = 0
                for i in range(0, size):
                    for j in range(0, size):
                        hashvalueleft = hashvalueleft + (mazeleft[i][j] << hashbit * 3)
                        hashbit += 1
                len1 = visitedboard.__len__()
                visitedboard.add(hashvalueleft)
                #if the hash is not in the set submit new solve
                if visitedboard.__len__() > len1:
#                    print mazeleft
#                    print "level " + str(level) +" - " + str(hashvalueleft)+ " added" + " Left"
#                    hashleft=True
                    pathleft = copy.deepcopy(path)
                    pathleft.append("L")
#                    print pathleft
                    ans,sol=solve(mazeleft, pathleft, level,matrixfinal)
                    visitedboard.remove(hashvalueleft)
                    if ans==True:
                        return True,sol
                
            elif (stroke == 3):
                for i in range(size-2,-1,-1):
                    for j in range(0, size):
                        if mazeright[j][i+1] == 0:
                            if (mazeright[j][i] != 1 and mazeright[j][i]!=100):
                                mazeright[j][i+1] = mazeright[j][i]
                                mazeright[j][i] = 0
                        if (mazeright[j][i+1] == 100):
                            if(mazeright[j][i] != 1 and mazeright[j][i] != 0):
                                mazeright[j][i+1] = 0
                                mazeright[j][i] = 0             
                # create the hash
                hashbit = 0
                hashvalueright = 0
                for i in range(0, size):
                    for j in range(0, size):
                        hashvalueright = hashvalueright + (mazeright[i][j] << hashbit * 3)
                        hashbit += 1
                len1 = visitedboard.__len__()
                visitedboard.add(hashvalueright)
                #if the hash is not in the set submit new solve
                if visitedboard.__len__() > len1:
#                    print mazeright
#                    print "level " + str(level) +" - " + str(hashvalueright)+ " added" + " Right"
#                    hashright=True
                    
                    pathright = copy.deepcopy(path)
                    pathright.append("R")
#                    print pathright
                    ans,sol=solve(mazeright, pathright, level,matrixfinal)
                    visitedboard.remove(hashvalueright)
                    if ans==True:
                        return True,sol
    return False,[]  


def createMaze(puzzle,dim):
    maze = []
    for row in range(dim):
        mazeRow = []
        for col in range(dim):
            index = (row*dim)+col
            mazeRow.append(int(puzzle[index]))
        maze.append(mazeRow)
    return maze



def createMazeFinal(matrixInitial,dim,matrixfinal):
     for row in range(dim):
        for col in range(dim):
           if matrixInitial[row][col]==1 and matrixfinal[row][col]==0:
               matrixfinal[row][col]=1
     return matrixfinal
 

def createMazeString(maze,dim):
    a=""
    for row in range(dim):
        for col in range(dim):
            if maze[row][col]==100:
                maze[row][col] = 'h'
            a = a+str(maze[row][col])
    return a

def findHole(matrix, dim):
    countShape = {2:0,3:0,4:0,5:0}
    for row in range(dim):
        for col in range(dim):
            if matrix[row][col]==2:
                countShape[2] = countShape[2] + 1
                if countShape[2] == 2:
                    return True,(row,col),2
            if matrix[row][col]==3:
                countShape[3] = countShape[3] + 1
                if countShape[3] == 2:
                    return True,(row,col),3
            if matrix[row][col]==4:
                countShape[4] = countShape[4] + 1
                if countShape[4] == 2:
                    return True,(row,col),4
            if matrix[row][col]==5:
                countShape[5] = countShape[5] + 1
                if countShape[5] == 2:
                    return True,(row,col),5
    return False,(0,0),0           
    

try:
    counter = 0  
    for puzzleTuple in data:
        puzzleInit = puzzleTuple[2]
        puzzleFinal = puzzleTuple[3]
        dim = int(len(puzzleInit) ** 0.5)  
        if problemCreatedCounter[dim] >= mazPuzzles:
            continue
        '''
        f=open("puzzleFinder5act.txt","a+")
        f.write(str(puzzleTuple[0]))
        f.write('\n')
        f.close()
        '''
        matrixInitial = createMaze(puzzleInit,dim)
        matrixfinal = createMaze(puzzleFinal,dim)
        matrixfinal = createMazeFinal(matrixInitial,dim,matrixfinal)
        find, hole, shape = findHole(matrixfinal, dim)
        if find == True:
            if matrixInitial[hole[0]][hole[1]] == 0:
                matrixInitial[hole[0]][hole[1]] = 100
                matrixfinal[hole[0]][hole[1]] = 0
                #print(matrixInitial)
                #print(matrixfinal)
                k=matrixInitial
                maxlimit = 8
                ans,path = solve(matrixInitial, [], 0, matrixfinal)
                if ans==True:
                    print(path)
                    print(puzzleTuple)
                    problemCreatedCounter[dim] = problemCreatedCounter[dim] +1
                    print(createMazeString(k,dim))
                    counter = counter + 1
                    z = str(counter)+','+str(createMazeString(k,dim))+','+str(createMazeString(matrixfinal,dim))+','+str(path)
                    f=open("hole.txt","a+")
                    f.write(z)
                    f.write('\n')
                    f.close()
               
                      
except Exception as e:
    print(str(e))
    '''
    f=open("puzzleFinder5act.txt","a+")
    f.write(str(e))
    f.write('\n')
    f.close()                  
    '''
    

curfull.close()       