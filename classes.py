import numpy
import math
import timeit
from random import shuffle

sim_time = 1

# current player is the player who will play the next move

class Stats:

    def __init__(self,parentSimCount):

        self.w = 0
        self.s = 0
        self.c = 0.5
        self.sp = parentSimCount

    def ucb(self):

        if s == 0:
            return 1000
        else:
            return (w/s) + (c*math.sqrt(math.log(sp)/s))

class Node:

    def __init__(self,player,opponent,parent = None,parentSimCount = 0):
        self.visited = False
        self.gameStats = Stats(parentSimCount)
        self.oppPlayer = opponent
        self.currPlayer = player
        self.nextMoves = []
        self.parentNode = parent

    def in_bound(x,y):
        if x < 8 and x > 0 and y > 0 and y < 8 :
            return true
        else:
            return false

    def allPossibleMoves(self):
        moves = []
        pieces = self.currPlayer.pieces
        oppPieces = self.oppPlayer.pieces
        
        for piece in pieces:
            x,y = piece

            if in_bound(x+1,y+1) and ((x+1,y+1) not in pieces) and ((x+1,y+1) not in oppPieces):
              
               temp_player = self.currPlayer
               temp_opponent = self.oppPlayer
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x+1,y+1))
               
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)
               
            if in_bound(x-1,y+1) and (x-1,y+1) not in pieces:
                
               temp_player = self.currPlayer
               temp_opponent = self.oppPlayer
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x-1,y+1))
               
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)
                
            if in_bound(x+1,y-1) and (x+1,y-1) not in pieces:
                
                
               temp_player = self.currPlayer
               temp_opponent = self.oppPlayer
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x+1,y-1))
               
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)
                
            if in_bound(x-1,y-1) and (x-1,y-1) not in pieces:
                
               temp_player = self.currPlayer
               temp_opponent = self.oppPlayer
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x-1,y-1))
               
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)

            if (x+1,y+1) in oppPieces and (x+2,y+2 not in pieces) and (x+2,y+2 not in oppPieces):
                
               temp_player = self.currPlayer
               temp_opponent = self.oppPlayer
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x+2,y+2))
               temp_opponent.pieces.remove((x+1,y+1))
               
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)
                
                
            if (x-1,y-1) in oppPieces and (x-2,y-2 not in pieces) and (x-2,y-2 not in oppPieces):
                
               temp_player = self.currPlayer
               temp_opponent = self.oppPlayer
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x-2,y-2))
               temp_opponent.pieces.remove((x-1,y-1))
               
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)
                
            if (x-1,y+1) in oppPieces and (x-2,y+2 not in pieces) and (x-2,y+2 not in oppPieces):
                
               temp_player = self.currPlayer
               temp_opponent = self.oppPlayer
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x-2,y+2))
               temp_opponent.pieces.remove((x-1,y+1))
               
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)
                
            if (x+1,y-1) in oppPieces and (x+2,y-2 not in pieces) and (x+2,y-2 not in oppPieces):
                
               temp_player = self.currPlayer
               temp_opponent = self.oppPlayer
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x+2,y-2))
               temp_opponent.pieces.remove((x+1,y-1))
               
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)


            return moves
        
        def simulate(self):
            
            curr_node = self
            winner = 0
            
            while true:
                
                if  len(curr_node.currPlayer.pieces) ==0 and len(curr_node.oppPlayer.pieces) !=0:
                    winner = curr_node.oppPlayer.playerId
                    break
                
                elif len(curr_node.currPlayer.pieces) !=0 and len(curr_node.oppPlayer.pieces) ==0:
                    winner = curr_node.currPlayer.playerId
                    break
                
                moves = curr_node.allPossibleMoves()
                shuffle(moves)
                
                curr_node = moves[0]
                
            return winner
            
            

class Tree:

    def __init__(self):
        self.root = Node(Player(1),Player(2))
        self.currNode = self.root

    def nextBestMove(self):

        if not self.currNode.nextMoves:
            self.currNode.nextMoves = self.currNode.allPossibleMoves()
        max_ucb = -1

        for node in self.currNode.nextMoves:
            if node.gameStats.ucb()>max_ucb:
                bestNode = node

        return bestNode

class Game:

    def setBoard(self):
        for loc in self.p1.pieces:
                self.board[loc] = 1
        for loc in self.p2.pieces:
                self.board[loc] = 2

    def play(self,player):
        print('playing')
        #todo

    def printBoard(self):
        print(self.board)

    def __init__(self):
        self.p1 = Player(1)
        self.p2 = Player(2)
        self.board = numpy.full((8,8),0)
        self.setBoard()
        self.status = 0
        self.gameTree = Tree()

    def play(self,playerId):
        
        start_time = timeit.default_timer()
        
        while timeit.default_timer < start_time + sim_time:
            
            current = self.gameTree.currNode
            while true:
        
                if current.gameStats.s == 0:
                    winner = current.simulate()
                    current.updateStats(winner)
                    break
                      
                else:
                    current = current.nextBestMove()
            
        
        self.gameTree.currNode = self.gameTree.currNode.nextBestMove()
        
class Player:

    def __init__(self,playerId):
        self.playerId = playerId
        self.pieces = []
        if playerId == 1:
            self.pieces.append((0,1))
            self.pieces.append((0,3))
            self.pieces.append((0,5))
            self.pieces.append((0,7))
            self.pieces.append((1,0))
            self.pieces.append((1,2))
            self.pieces.append((1,4))
            self.pieces.append((1,6))
            self.pieces.append((2,1))
            self.pieces.append((2,3))
            self.pieces.append((2,5))
            self.pieces.append((2,7))

        if playerId == 2:
            self.pieces.append((5,0))
            self.pieces.append((5,2))
            self.pieces.append((5,4))
            self.pieces.append((5,6))
            self.pieces.append((6,1))
            self.pieces.append((6,3))
            self.pieces.append((6,5))
            self.pieces.append((6,7))
            self.pieces.append((7,0))
            self.pieces.append((7,2))
            self.pieces.append((7,4))
            self.pieces.append((7,6))
