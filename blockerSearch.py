# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:32:01 2019

@author: siddharth
"""

import time
import copy

# a = 0: free, 1: block 2: pawn_1 3: pawn_2 4: pawn_3 5: pawn_4 6: Pawn_5 7: Pawn_6 8: pawn_6
visitedboard=set()
matrixInitial = [[2,0,0],[3,3,0],[1,0,2]]
matrixfinal = [[0,2,2],[0,3,0],[1,3,0]]
maxlimit=20
size=len(matrixfinal)



def solve(maze, path, level):
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
                print(path)
                print("No of moves",path.__len__())
                print(time.time()-a)
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
                    solve(mazeup, pathup, level)
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
                    solve(mazedown, pathdown, level)
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
                    solve(mazeleft, pathleft, level)
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
                    solve(mazeright, pathright, level)
                    visitedboard.remove(hashvalueright)


for row in range(len(matrixInitial)):
    for col in range(len(matrixInitial)):
        if matrixInitial[row][col] == 0 and matrixfinal[row][col]==0:
            print(matrixInitial)
            matrixInitial[row][col] = 1
            matrixfinal[row][col] = 1
            print(matrixInitial)
            a=time.time()
            solve(matrixInitial,[],0)
            matrixInitial[row][col] = 0
            matrixfinal[row][col] = 0
            print("------")
                
            
            
