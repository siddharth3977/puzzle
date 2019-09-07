# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 19:25:21 2019

@author: siddharth
"""

from pymongo import MongoClient
import datetime
import time
import logging 

logging.basicConfig(filename="gameScoring.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 

logger=logging.getLogger() 
logger.setLevel(logging.INFO) 

client = MongoClient()
client = MongoClient('localhost', 27017)

db = client['sync-test']
game= db['games']

def calculateUserScore(userPuzzleStats, puzzleTime, puzzleMoves):
    score = 0
    for stats in userPuzzleStats:
        puzzleId = stats['puzzleId']
        movesContribution = 0
        timeContribution = 0
        if stats['countOfMoves'] > 0:
            movesContribution = puzzleMoves[puzzleId]/stats['countOfMoves']
        if puzzleTime[puzzleId] > 0:
            timeContribution = 1 - (stats['timeTaken']/puzzleTime[puzzleId])
        puzScore = (movesContribution + timeContribution)/2
        score = score + puzScore
    return score
    

def computeScore(game):
    puzzleList=game['puzzles']
    puzzle = db['puzzles']
    puzzleObj = puzzle.find({'_id':{'$in':puzzleList}})
    puzzleTime = {}
    puzzleMoves = {}
    for p in puzzleObj:
        puzzleTime[p['puzzleId']] = p['maxTime']
        puzzleMoves[p['puzzleId']] = p['perfectSolutionLength']
    gameStats = db['gamesStats']
    gameStatsObj = gameStats.find({'gameId':game['gameId']})
    newGameStatsObj = []
    logger.info("Computing score for players gameId : %s",game['gameId'])
    for s in gameStatsObj:
        score = calculateUserScore(s['puzzleStats'], puzzleTime, puzzleMoves)
        newGameStatsObj.append(s)
        s['score'] = score
    logger.info("Sorting score for gameId : %s",game['gameId'])
    sortedGameStats = sorted(newGameStatsObj, key=lambda x:(-x['score'],x['createdAt']))  
    rank =1
    logger.info("Ranking players for gameId : %s",game['gameId'])
    for s in sortedGameStats:
        s['rank'] = rank
        rank = rank + 1
    logger.info("Updating user stats for gameId : %s",game['gameId'])    
    for s in sortedGameStats:
        whereQuery = { "_id": s['_id'] }
        newValues = { "$set": s }
        gameStats.update_one(whereQuery, newValues)

def updateGame(gameDict):
    whereQuery = { "gameId": gameDict['gameId'] }
    newValues = { "$set": {'evaluated':True} }
    game.update_one(whereQuery, newValues)
            

def checkGames():
    while(True):
        computeTime = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
        gameObj = game.find({'evaluated':False,'end':{'$lt':computeTime}})
        if gameObj.count() == 0:
            logger.info("Sleeping for 5 min")
            time.sleep(300)
            continue
        for g in gameObj:
            logger.info("Starting score computation for gameId : %s",g['gameId'])
            computeScore(g)
            logger.info("Finished score computation for gameId : %s",g['gameId'])
            updateGame(g)
            logger.info("Setting evaluated to True for gameId : %s",g['gameId'])
  
        

def startBatch():
    try:
        checkGames()
    except Exception as e:
        print(str(e))
        client.close()
    
      
if __name__=="__main__":
    startBatch()


