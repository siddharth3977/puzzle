# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 07:47:45 2019

@author: siddharth
"""

import copy
import sqlite3 as lite

blockerPuzzle = []
mazPuzzles = 10
problemCreatedCounter = {3:20,4:20,5:0,6:20,7:20}
confull = lite.connect('DB_GameData.db')
curfull= confull.cursor()
curfull.execute('select * from puzzles')
data = curfull.fetchall()

# a = 0: free, 1: block 2: pawn_1 3: pawn_2 4: pawn_3 5: pawn_4 6: Pawn_5 7: Pawn_6 8: pawn_6
visitedboard=set()

maxlimit=20
f= open("guru9109.txt","w+")

def solve(maze, path, level,matrixfinal):
    size=len(matrixfinal)
    global visitedboard,maxlimit
   
    Found = True

    for i in range(0, size):
        for j in range(0,size):
            if ((maze[i][j]> 1) and ( maze[i][j] != matrixfinal[i][j])):
                Found = False
    if Found:
        if ( level == 0):
            return False
        else:
            if (path.__len__()< maxlimit):
                #print(path)
                #print("No of moves",path.__len__())
                maxlimit=path.__len__()
                return True
        return False
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
                len1 = visitedboard.__len__()
                visitedboard.add(hashvalueup)
                #if the hash is not in the set submit new solve
                if visitedboard.__len__() > len1:
#
                    pathup = copy.deepcopy(path)
                    pathup.append("U")
#                    print pathup
                    ans = solve(mazeup, pathup, level,matrixfinal)
                    visitedboard.remove(hashvalueup)
                    if ans==True:
                        return True

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
                    ans=solve(mazedown, pathdown, level,matrixfinal)
                    visitedboard.remove(hashvaluedown)
                    if ans==True:
                        return True
               

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
                    ans=solve(mazeleft, pathleft, level,matrixfinal)
                    visitedboard.remove(hashvalueleft)
                    if ans==True:
                        return True
                
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
                    ans=solve(mazeright, pathright, level,matrixfinal)
                    visitedboard.remove(hashvalueright)
                    if ans==True:
                        return True
    return False                    

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
    


counter = 0  
for puzzleTuple in data:
    #if int(puzzleTuple[0])<343:
     #   continue
    print("---------------------------------")
    print(puzzleTuple)
    puzzleInit = puzzleTuple[2]
    puzzleFinal = puzzleTuple[3]
    dim = int(len(puzzleInit) ** 0.5)  
    if problemCreatedCounter[dim] >= mazPuzzles:
        #break
        continue
    matrixInitial = createMaze(puzzleInit,dim)
    matrixfinal = createMaze(puzzleFinal,dim)
    matrixfinal = createMazeFinal(matrixInitial,dim,matrixfinal)
    blockerFound = False
    for row in range(len(matrixInitial)):
        if blockerFound == True:
            break
        for col in range(len(matrixInitial)):
            if matrixInitial[row][col] == 0 and matrixfinal[row][col]==0:
                print("going to find chnaging block")
                print("row is",row)
                print("col is",col)
                print("initial matrix",matrixInitial)
                print("final matrix",matrixfinal)
                matrixInitial[row][col] = 1
                matrixfinal[row][col] = 1
                maxlimit = 20
                print("after change")
                print("initial matrix",matrixInitial)
                print("final matrix",matrixfinal)
                ans = solve(matrixInitial,[],0,matrixfinal)
                matrixInitial[row][col] = 0
                matrixfinal[row][col] = 0
                if ans==False:
                    blockerFound = True
                    blockerPuz = list(puzzleInit)
                    blockerPuz[(row*dim)+col] = 'b'
                    blockerPuz="".join(blockerPuz)
                    problemCreatedCounter[dim] = problemCreatedCounter[dim] +1
                    counter = counter + 1
                    blockerPuzzle.append((counter,puzzleTuple[0],puzzleInit,puzzleFinal,blockerPuz,puzzleTuple[4]))  
                    z = str(counter)+','+str(puzzleTuple[0])+','+str(puzzleInit)+','+str(puzzleFinal)+','+str(blockerPuz)+','+str(puzzleTuple[4])
                    f.write(z)
                    f.write('\n')
                    print(blockerPuzzle)
                    break

print(problemCreatedCounter)
print(blockerPuzzle)
curfull.close()                
f.close()