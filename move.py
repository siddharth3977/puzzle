from __future__ import print_function
import sys
import random
from random import randint
import sqlite3 as lite
import copy

# a = 0: free, 1: block 2: pawn_1 3: pawn_2 4: pawn_3 5: pawn_4 6: Pawn_5 7: Pawn_6 8: pawn_6

def initializeMatrix(size, colors, pawns):
    global matrixinitial, matrixfinal, visited,maxlimit
    matrixfinaltemp =  [x[:] for x in [[0] * size] * size]
    for i in range(0,size):
        for j in range(0,size):
            matrixfinal[i][j]=0
            matrixinitial[i][j]=0
    freecells_i = []
    freecells_f = []
    for i in range(0, size * size):
        freecells_i.append(i)
        freecells_f.append(i)
    # determine the color distribution among pawn
    entries = []
    i = 0
    j = -1  # color ranges from 2-8
    while ( i < pawns):
        j = (( j + 1) % colors)   # 0 and 1 are reservered for free and block
        entries.append(j+2)
        i = i + 1

    #determine how many blockers required
    multiplier = random.choice([0.3, 0.4, 0.5])
    blockers = int(( size * size - pawns ) * multiplier)
    for i in range(0, blockers):
        entries.append(1)
    # remaining are free cells

    # Fill matrixinitial

    for i in entries:
        index = random.sample(freecells_i, 1)[0]
        freecells_i.remove(index)
        if i == 1:  # if this entry is blocking type
            freecells_f.remove(index)
        row = index / size
        col = index % size
        matrixinitial[row][col] = i
    # calculate hash for matrixinitial
    hashbit = 0
    hashvalueini = 0
    for i in range(0, size):
        for j in range(0, size):
            hashvalueini = hashvalueini + (matrixinitial[i][j] << hashbit * 3)
            hashbit += 1

    if (size < 4):
   # Fill matrixfinal in old way

        for j in entries:
            if (j != 1):  ## skip if blocked
                index = random.sample(freecells_f, 1)[0]
                freecells_f.remove(index)
                row = index / size
                col = index % size
                matrixfinal[row][col] = j
    else:

# initialize matrixfinal with matrixinitial
        matrixfinal=[row[:] for row in matrixinitial]
        matrixfinaltemp = [row[:] for row in matrixfinal]
# get ramdom number of moves between 3-13
#        applymoves =  randint( 3,20)
        applymoves = maxlimit+4
        if (maxlimit > 15 ):
            maxlimit=15
# Apply the selected number of moves valid moves in matrixfinal

        for m in range(0,applymoves):
            moves=[0,1,2,3]
            random.shuffle(moves)
            progress= False
            for n in moves:
                if (n == 0):  # upper stroke
                    for i in range(1, size):
                        for j in range(0, size):
                            if (matrixfinaltemp[i - 1][j] == 0):
                                if (matrixfinaltemp[i][j] != 1):
                                    matrixfinaltemp[i - 1][j] = matrixfinaltemp[i][j]
                                    matrixfinaltemp[i][j] = 0
                elif (n == 1):  # down stroke
                    for i in range(size - 2, -1, -1):
                        for j in range(0, size):
                            if (matrixfinaltemp[i + 1][j] == 0):
                                if (matrixfinaltemp[i][j] != 1):
                                    matrixfinaltemp[i + 1][j] = matrixfinaltemp[i][j]
                                    matrixfinaltemp[i][j] = 0
                elif (n == 2):  #left stroke
                    j = 0
                    for n in range(0, size-1):
                        i=-1
                        j = j + 1
                        for m in range(0, size):  # loop to create same column
                            i=i+1
                            if matrixfinaltemp[i][j-1] == 0:
                                if matrixfinaltemp[i][j] != 1:
                                    matrixfinaltemp[i ][j-1] = matrixfinaltemp[i][j]
                                    matrixfinaltemp[i][j] = 0
                elif (n == 3):
                    j = size-1
                    for n in range(0, size-1):
                        i=-1
                        j=j-1
                        for m in range(0, size):
                            i+=1
                            if matrixfinaltemp[i ][j+1] == 0:
                                if matrixfinaltemp[i][j] != 1:
                                    matrixfinaltemp[i][j+1] = matrixfinaltemp[i][j]
                                    matrixfinaltemp[i][j] = 0

                if ( matrixfinal!=matrixfinaltemp):
                    progress = True
                    matrixfinal = [row[:] for row in matrixfinaltemp]
                    break
            if ( not progress):
                return False

# calculate hash for matrixfinal
    hashbit = 0
    hashvaluefinal = 0
    for i in range(0, size):
            for j in range(0, size):
                hashvaluefinal = hashvaluefinal + (matrixfinal[i][j] << hashbit * 3)
                hashbit += 1
    len = visited.__len__()
    visited.add((hashvalueini, hashvaluefinal))
    # Test Board
    if visited.__len__() > len:
            return True
    else:
            return False


def solve(maze, path, level):
    global matrixfinal, visitedboard,counter, maxlimit
    mazeupcheck = mazedowncheck = mazeleftcheck = mazerightcheck = True
    counter+=1
#    if counter%10000==0:
#        print counter
    Found = True
#    print "level " + str(level+1) + "   Entry Maze "+ str(maze)
    for i in range(0, size):
        for j in range(0,size):
            if ((maze[i][j]> 1) and ( maze[i][j] != matrixfinal[i][j])):
                Found = False
    if Found:
        if ( level == 0):
            return False
        else:
            if (path.__len__()< maxlimit):
                result.append(path)
                maxlimit=path.__len__()
        return True
    else:
        level += 1
        if (level > maxlimit):  #  need not require more than 20 strokes overall
            return False
        # create 4 mazecopy
        hashup=hashdown=hashleft=hashright=False
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
#                    print mazeup
#                    print "level " + str(level) +" - " + str(hashvalueup)+ " added" + " Up"
#                    hashup = True
                    pathup = copy.deepcopy(path)
                    pathup.append(0)
#                    print pathup
                    retup = solve(mazeup, pathup, level)
                    visitedboard.remove(hashvalueup)
                else:
#                    print mazeup
#                    print "level " + str(level) +" - " + str(hashvalueup)+ " dup " + " Up"
                    retup = False


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
                    pathdown.append(1)
#                    print pathdown
                    retdown = solve(mazedown, pathdown, level)
                    visitedboard.remove(hashvaluedown)
                else:
#                    print mazedown
#                    print "level " + str(level) +" - " + str(hashvaluedown)+ " dup " + " Down"
                    retdown = False


            elif (stroke == 2):  #left stroke
                j = 0
                for n in range(0, size-1):
                    i=-1
                    j = j + 1
                    for m in range(0, size):  # loop to create same column
                        i=i+1
                        if mazeleft[i][j-1] == 0:
                            if mazeleft[i][j] != 1:
                                mazeleft[i ][j-1] = mazeleft[i][j]
                                mazeleft[i][j] = 0
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
                    pathleft.append(2)
#                    print pathleft
                    retleft = solve(mazeleft, pathleft, level)
                    visitedboard.remove(hashvalueleft)
                else:
#                    print mazeleft
#                    print "level " + str(level) +" - " + str(hashvalueleft)+ " Dup" + " Left"
                    retleft = False
            elif (stroke == 3):
                j = size-1
                for n in range(0, size-1):
                    i=-1
                    j=j-1
                    for m in range(0, size):
                        i+=1
                        if mazeright[i ][j+1] == 0:
                            if mazeright[i][j] != 1:
                                mazeright[i][j+1] = mazeright[i][j]
                                mazeright[i][j] = 0
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
                    a =  path.__len__()
                    pathright = copy.deepcopy(path)
                    pathright.append(3)
#                    print pathright
                    retright = solve(mazeright, pathright, level)
                    visitedboard.remove(hashvalueright)
                else:
#                    print mazeright
#                    print "level " + str(level) +" - " + str(hashvalueright)+ " Dup" + " Right"
                    retright = False
def readsqldata():

    global matrixinitial, matrixfinal, visited,maxlimit, Noofboards, readresult,databaserecordno
    # ReadOnce and get Noofboards
    # Maintain a nextboard and if it is >1 and then read the next board into matrixinitial and matrixfinal, size,colors,pawn
    # create readresult[] to compare with result of solve
    return True


#read
# initialize global variables
for colors in range ( 2,6):
    for MovesRequired in range(8,13):
        size = 6
#        colors =1
        pawns = 8
        #    MovesRequired= 5
        Noofboards= 10
        visited = set()
        visitedboard = set()
        #    f=open("C:\\Users\\ssarma\\Documents\\Working_Folder\\Nonproject\\personal\\BBS\Move\\result_size%d__pawns%d_colors%d_Moves%d_Board%d.txt" % (size,pawns, colors,MovesRequired,Noofboards), "w")

        # initialize matrix and freecells
        matrixinitial = [x[:] for x in [[0] * size] * size]
        matrixfinal = matrix = [x[:] for x in [[0] * size] * size]
        freecells = []
        boardcount=0
        for i in range(0, size * size):
            freecells.append(i)
        conupdated = lite.connect('C:\\Users\\ssarma\\Documents\\Working_Folder\\Nonproject\\personal\\BBS\Move\\sync_updated.db')
        curupdated = conupdated.cursor()

        for k in range(0, 3000):
            path = []
            result = []
            counter=0
            maxlimit =MovesRequired+1
            if (initializeMatrix(size, colors, pawns)):
                # add the new board to visitedboard
                visitedboard.clear()
                hashbit = 0
                hashvalueini = 0
                for i in range(0, size):
                    for j in range(0, size):
                        hashvalueini = hashvalueini + (matrixinitial[i][j] << hashbit * 3)
                        hashbit += 1
                visitedboard.add(hashvalueini)
                #recusively try to solve the board
                solve(matrixinitial, path, 0)
                #            print ("loop: "+str(size)+str(colors)+str(pawns)+" progress: "+str(k), file=sys.stdout)
                resultlen=result.__len__()
                if (resultlen > 0):
                    print ("loop: "+str(size)+str(colors)+str(pawns)+" progress: "+str(k), file=sys.stdout)
                    resultindex=0
                    for m in range(1, resultlen):
                        if ( result[m].__len__() < result[resultindex].__len__()):
                            resultindex=m
                    if (result[resultindex].__len__() == MovesRequired):
                        boardcount+=1
                        #                    print (size, len(result[resultindex]), matrixinitial, matrixfinal, result[resultindex], file=f)
                        #                    sys.stdout.flush()
                        unsolvedrow=''
                        solvedrow=''
                        for k in range(0,size):
                            unsolvedrow=unsolvedrow+''.join(map(str, matrixinitial[k]))
                            solvedrow=solvedrow+''.join(map(str, matrixfinal[k]))
                        solutionrow=''.join(map(str, result[resultindex]))
                        curupdated.execute("SELECT * FROM BASE_SYNC WHERE Unsolved=? and Solved=?",(unsolvedrow,solvedrow))
                        rowupdatednotexists=curupdated.fetchall()
                        if (len(rowupdatednotexists)>0):
                            continue
                        else:
                            curupdated.execute("insert into ADV_SYNC values (?,?,?,?,?,?,?,?,?,?,?)",(pawns,colors,size, MovesRequired,unsolvedrow,solvedrow,solutionrow,'1_0','5','0','0'))
                            conupdated.commit()

            if ( boardcount>=Noofboards):
                break
exit(0)
i=False
if (i==True):   #this is the case for board validation

    conupdated = None
    confull= None
    conunupdated =None

    try:
        conupdated = lite.connect('C:\\Users\\ssarma\\Documents\\Working_Folder\\Nonproject\\personal\\BBS\Move\\sync_updated.db')
        curupdated = conupdated.cursor()
        confull = lite.connect('C:\\Users\\ssarma\\Documents\\Working_Folder\\Nonproject\\personal\\BBS\Move\\sync_full.db')
        curfull= confull.cursor()
        conunupdated = lite.connect('C:\\Users\\ssarma\\Documents\\Working_Folder\\Nonproject\\personal\\BBS\Move\\sync_unupdated.db')
        curunupdated = conunupdated.cursor()
        curupdated.execute('SELECT SQLITE_VERSION()')
        data = curupdated.fetchone()
        print ("SQLite version: %s" % data,file=sys.stdout)
    except lite.Error, e:
        print ("Error %s:" % e.args[0],file=sys.stdout)
        sys.exit(1)
    with conupdated:

        curupdated = conupdated.cursor()
#        cur.execute("alter table BASE_SYNC add column `modified` integer")
        curupdated.execute("SELECT * FROM BASE_SYNC")
#        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        names = [description[0] for description in curupdated.description]
        rows = curupdated.fetchall()
        databaserecordno=0
        for row in rows:
#            databaserecordno=databaserecordno+1
#            if (row[8]==2):
#                print (databaserecordno,row, file=sys.stdout)
#                continue
#            else:
#                continue
#       i=True
#       if (i==False):
            size = row[2]
            colors =row[1]
            pawns = row[0]
            move1=row[3]
            unsolved = row[4]
            solved=row[5]
            solution=row[6]
            modified=row[8]
            databaserecordno+=1
            if (modified==1):
                print(row,file=sys.stdout)
                # get the corresponding entry from curunupdated and get number of move2
                curunupdated = conunupdated.cursor()
                curunupdated.execute("SELECT * FROM BASE_SYNC WHERE Unsolved=? and Solved=?",(unsolved,solved ))
                rowunupdated = curunupdated.fetchall()
                moves2= rowunupdated[0][3]
                print( "moves from unupdated:"+str(moves2), file=sys.stdout)
                # if move1==move2 then continue
                if ( move1!=moves2):
                    curfull=confull.cursor()
                    # else open database in sync_full and table SYNC_%dx%d_%d_%d ( size,size, pawns,colors)
                    if (size==3 and pawns==2 and colors==1 ):
                            curfull.execute("SELECT * FROM SYNC_3x3_2_1 WHERE Moves=?",str(moves2))
                    elif (size==3 and pawns==2 and colors==2 ):
                            curfull.execute("SELECT * FROM SYNC_3x3_2_2 WHERE Moves=?",str(moves2))
                    elif (size==3 and pawns==3 and colors==2 ):
                            curfull.execute("SELECT * FROM SYNC_3x3_3_2 WHERE Moves=?",str(moves2))
                    elif (size==3 and pawns==3 and colors==3 ):
                            curfull.execute("SELECT * FROM SYNC_3x3_3_3 WHERE Moves=?",str(moves2))
                    elif (size==3 and pawns==4 and colors==2 ):
                            curfull.execute("SELECT * FROM SYNC_3x3_4_2 WHERE Moves=?",str(moves2))
                    elif (size==3 and pawns==4 and colors==3 ):
                            curfull.execute("SELECT * FROM SYNC_3x3_4_3 WHERE Moves=?",str(moves2))
                    elif (size==3 and pawns==4 and colors==4 ):
                            curfull.execute("SELECT * FROM SYNC_3x3_4_4 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==4 and colors==1 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_4_1 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==4 and colors==2 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_4_2 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==4 and colors==3 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_4_3 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==4 and colors==4 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_4_4 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==5 and colors==1 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_5_1 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==5 and colors==2 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_5_2 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==5 and colors==3 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_5_3 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==5 and colors==4 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_5_4 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==5 and colors==5 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_5_5 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==6 and colors==1 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_6_1 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==6 and colors==2 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_6_2 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==6 and colors==3 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_6_3 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==6 and colors==4 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_6_4 WHERE Moves=?",str(moves2))
                    elif (size==4 and pawns==6 and colors==5 ):
                            curfull.execute("SELECT * FROM SYNC_4x4_6_5 WHERE Moves=?",str(moves2))
                    elif (size==5 and pawns==6 and colors==1 ):
                            curfull.execute("SELECT * FROM SYNC_5x5_6_1 WHERE Moves=?",str(moves2))
                    elif (size==5 and pawns==6 and colors==2 ):
                            curfull.execute("SELECT * FROM SYNC_5x5_6_2 WHERE Moves=?",str(moves2))
                    elif (size==5 and pawns==6 and colors==3 ):
                            curfull.execute("SELECT * FROM SYNC_5x5_6_3 WHERE Moves=?",str(moves2))
                    elif (size==5 and pawns==6 and colors==4 ):
                            curfull.execute("SELECT * FROM SYNC_5x5_6_4 WHERE Moves=?",str(moves2))
                    elif (size==5 and pawns==6 and colors==5 ):
                            curfull.execute("SELECT * FROM SYNC_5x5_6_5 WHERE Moves=?",str(moves2))
                    elif (size==5 and pawns==6 and colors==6 ):
                            curfull.execute("SELECT * FROM SYNC_5x5_6_6 WHERE Moves=?",str(moves2))
                    else:
                            break


                    rowsfull = curfull.fetchall()
                    for rowfull in rowsfull:
                        # Ensure that check if rowfull not in database
#                        curupdated.cursor()
                        unsolvedrow=rowfull[4]
                        solvedrow=rowfull[5]
                        solutionrow=rowfull[6]
                        curupdated.execute("SELECT * FROM BASE_SYNC WHERE Unsolved=? and Solved=?",(unsolvedrow,solvedrow))
                        rowupdatednotexists=curupdated.fetchall()
                        if (len(rowupdatednotexists) !=0):
                                continue
                        else:
                            # compare if there is a correct solution exists with solve

                # Get any any with move2
                # validate with solve that move2 remain
                # update it in curupdated
                            matrixinitial = [x[:] for x in [[0] * size] * size]
                            matrixfinal = matrix = [x[:] for x in [[0] * size] * size]
                            readresult= []
                            for i1 in range(0,size):
                                    for j1 in range (0,size):
                                        matrixfinal[i1][j1]=int(solvedrow[size*i1+j1])
                            for i1 in range(0,size):
                                    for j1 in range (0,size):
                                        matrixinitial[i1][j1]=int(unsolvedrow[size*i1+j1])
                            for d in solutionrow:
                                readresult.append(int(d))
                            path = []
                            result = []
                            counter=0
                            maxlimit=10
                            visited = set()
                            visitedboard = set()
                            visitedboard.clear()
                            hashbit = 0
                            hashvalueini = 0
                            for i in range(0, size):
                                for j in range(0, size):
                                    hashvalueini = hashvalueini + (matrixinitial[i][j] << hashbit * 3)
                                    hashbit += 1
                            visitedboard.add(hashvalueini)
                            solve(matrixinitial,path,0)
                            resultlen=result.__len__()
                            if (resultlen > 1):
                                resultindex=0
                            else:
                                continue
                            for m in range(1, resultlen):
                                    if ( result[m].__len__() < result[resultindex].__len__()):
                                        resultindex=m

                            #compare result with readresult
                            if (len(result[resultindex]) == len(readresult)):
#                                    resulty=''.join(map(str, result[m]))
                                    print (databaserecordno,result[m],readresult, file=sys.stdout)
                                    curupdated.execute("UPDATE BASE_SYNC SET Solution=? WHERE Unsolved=? and Solved=?",(solutionrow,unsolved,solved ))
                                    curupdated.execute("UPDATE BASE_SYNC SET uUnsolved=? WHERE Unsolved=? and Solved=?",(unsolvedrow,unsolved,solved ))
                                    curupdated.execute("UPDATE BASE_SYNC SET uSolved=? WHERE Unsolved=? and Solved=?",(solvedrow,unsolved,solved ))
                                    curupdated.execute("UPDATE BASE_SYNC SET modified=? WHERE Unsolved=? and Solved=?",('4',unsolved,solved ))
                                    curupdated.execute("UPDATE BASE_SYNC SET Moves=? WHERE Unsolved=? and Solved=?",(moves2,unsolved,solved ))
                                    conupdated.commit()
                                    break
                            else:
                                    continue

                else:
                    continue