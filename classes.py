import numpy
import math
import timeit
from random import shuffle
import copy

sim_time = 1

def in_bound(x,y):
    if x < 8 and x >= 0 and y >= 0 and y < 8 :
        return True
    else:
        return False

# current player is the player who will play the next move
# stats of player 1 are stores
class Stats:

    def __init__(self,parentSimCount):

        self.w = 0
        self.s = 0
        self.c = 0.5
        self.sp = parentSimCount

    def ucb(self):

        if self.s == 0:
            return 1000
        else:
            return (self.w/self.s) + (self.c*math.sqrt(math.log(self.sp + 1)/self.s))

    def probability(self):

        if self.s == 0:
            return 0
        else:
            return (self.w/self.s)


class Node:

    def __init__(self,player,opponent,parent = None,parentSimCount = 0):
        self.visited = False
        self.gameStats = Stats(parentSimCount)
        self.oppPlayer = opponent
        self.currPlayer = player
        self.nextMoves = []
        self.parentNode = parent

    def printBoard(self):
        currBoard = numpy.full((8,8),0)
        for piece in self.currPlayer.pieces:
            currBoard[piece] = self.currPlayer.playerId

        for piece in self.oppPlayer.pieces:
            currBoard[piece] = self.oppPlayer.playerId

        print(currBoard)


    def allPossibleMoves(self,p):
        moves = []
        pieces = self.currPlayer.pieces
        oppPieces = self.oppPlayer.pieces
        isKing = self.currPlayer.isKing

        for piece in pieces:
            x,y = piece
            piece_index = pieces.index(piece)
            prev_len_player = len(pieces)
            prev_len_opp = len(oppPieces)
            if in_bound(x+1,y+1) and ((x+1,y+1) not in pieces) and ((x+1,y+1) not in oppPieces) and (self.currPlayer.playerId == 1 or (isKing[piece_index] ==1)):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x+1,y+1))
               temp_player.updateKings()

               if p == 1:
                   print((x,y),(x+1,y+1))
               if len(temp_player.pieces) == prev_len_player and len(temp_opponent.pieces) == prev_len_opp :
                   new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
                   moves.append(new_node)

            if in_bound(x-1,y-1) and ((x-1,y-1) not in pieces) and ((x-1,y-1) not in oppPieces) and (self.currPlayer.playerId == 2 or (isKing[piece_index] == 1)):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x-1,y-1))
               temp_player.updateKings()
               if len(temp_player.pieces) == prev_len_player and len(temp_opponent.pieces) == prev_len_opp :
                   new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
                   moves.append(new_node)

            if in_bound(x+1,y-1) and ((x+1,y-1) not in pieces) and ((x+1,y-1) not in oppPieces) and (self.currPlayer.playerId == 1 or (isKing[piece_index] == 1)):


               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x+1,y-1))
               temp_player.updateKings()
               if len(temp_player.pieces) == prev_len_player and len(temp_opponent.pieces) == prev_len_opp :
                   new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
                   moves.append(new_node)

            if in_bound(x-1,y+1) and ((x-1,y+1) not in pieces) and ((x-1,y+1) not in oppPieces) and (self.currPlayer.playerId == 2 or (isKing[piece_index] == 1)):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x-1,y+1))
               temp_player.updateKings()
               if len(temp_player.pieces) == prev_len_player and len(temp_opponent.pieces) == prev_len_opp :
                   new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
                   moves.append(new_node)

            if in_bound(x+2,y+2) and ((x+1,y+1) in oppPieces) and ((x+2,y+2) not in pieces) and ((x+2,y+2) not in oppPieces) and (self.currPlayer.playerId == 1 or (isKing[piece_index] == 1)):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x+2,y+2))
               temp_opponent.isKing.pop(temp_opponent.pieces.index((x+1,y+1)))
               temp_opponent.pieces.remove((x+1,y+1))
               temp_player.updateKings()
               if len(temp_player.pieces) == prev_len_player and len(temp_opponent.pieces) == prev_len_opp - 1 :
                   new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
                   moves.append(new_node)


            if in_bound(x-2,y-2) and ((x-1,y-1) in oppPieces) and ((x-2,y-2) not in pieces) and ((x-2,y-2) not in oppPieces) and (self.currPlayer.playerId == 2 or (isKing[piece_index] == 1)):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x-2,y-2))
               temp_opponent.isKing.pop(temp_opponent.pieces.index((x-1,y-1)))
               temp_opponent.pieces.remove((x-1,y-1))
               temp_player.updateKings()
               if len(temp_player.pieces) == prev_len_player and len(temp_opponent.pieces) == prev_len_opp - 1 :
                   new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
                   moves.append(new_node)

            if in_bound(x-2,y+2) and ((x-1,y+1) in oppPieces) and ((x-2,y+2) not in pieces) and ((x-2,y+2) not in oppPieces) and (self.currPlayer.playerId == 2 or (isKing[piece_index] == 1)):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x-2,y+2))
               temp_opponent.isKing.pop(temp_opponent.pieces.index((x-1,y+1)))
               temp_opponent.pieces.remove((x-1,y+1))
               temp_player.updateKings()
               if len(temp_player.pieces) == prev_len_player and len(temp_opponent.pieces) == prev_len_opp - 1 :
                   new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
                   moves.append(new_node)

            if in_bound(x+2,y-2) and ((x+1,y-1) in oppPieces) and ((x+2,y-2) not in pieces) and ((x+2,y-2) not in oppPieces) and (self.currPlayer.playerId == 1 or (isKing[piece_index] == 1)):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces.remove((x,y))
               temp_player.pieces.append((x+2,y-2))
               temp_opponent.isKing.pop(temp_opponent.pieces.index((x+1,y-1)))
               temp_opponent.pieces.remove((x+1,y-1))
               temp_player.updateKings()
               if len(temp_player.pieces) == prev_len_player and len(temp_opponent.pieces) == prev_len_opp - 1 :
                   new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
                   moves.append(new_node)

        return moves


    def updateStats(self,winner):

        self.gameStats.s = self.gameStats.s + 1

        if(winner == 1):
            self.gameStats.w = self.gameStats.w + 1

        if(self.parentNode == None):
            return
        else:
            self.parentNode.updateStats(winner)
            return

    def simulate(self):

        curr_node = self
        winner = 0
        start_time = timeit.default_timer()
        while timeit.default_timer() < start_time + 1:

            if  len(curr_node.currPlayer.pieces) ==0 and len(curr_node.oppPlayer.pieces) !=0:
                winner = curr_node.oppPlayer.playerId
                break

            elif len(curr_node.currPlayer.pieces) !=0 and len(curr_node.oppPlayer.pieces) ==0:
                winner = curr_node.currPlayer.playerId
                break

            moves = curr_node.allPossibleMoves(0)
            shuffle(moves)

            if len(moves) != 0:
                curr_node = moves[0]
            else:
                winner = curr_node.oppPlayer.playerId
                break

        return winner

    def nextBestMove(self):

        #print "Finding next best move"
        if not self.nextMoves:
            self.nextMoves = self.allPossibleMoves(0)
        max_ucb = -1
        if len(self.nextMoves) == 0:
            return self.oppPlayer.playerId
        #print "length of nextmove:", len(self.nextMoves)
        for node in self.nextMoves:
            if node.gameStats.ucb()>max_ucb:
                bestNode = node

        return bestNode


class Tree:

    def __init__(self):
        self.root = Node(Player(1),Player(2))
        self.currNode = self.root


    def nextBestPlay(self):

        if not self.currNode.nextMoves:
            self.currNode.nextMoves = self.currNode.allPossibleMoves(1)
        max_prob= -1
        min_prob = 5000

        if len(self.currNode.nextMoves) == 0:
            return self.currNode.oppPlayer.playerId

        # if self.currNode.oppPlayer.playerId == 2 :
        #     shuffle(self.currNode.nextMoves)
        #     return self.currNode.nextMoves[0]

        for node in self.currNode.nextMoves:
            if node.gameStats.probability()>max_prob:
                bestPlay = node
            if node.gameStats.probability()<min_prob:
                worstPlay = node


        if self.currNode.currPlayer.playerId == 1:
            return bestPlay
        else:
            return worstPlay

class Game:

    def __init__(self):
        self.p1 = Player(1)
        self.p2 = Player(2)
        self.status = 0
        self.gameTree = Tree()

    def getStatus(self):

        winner = 0
        curr_node = self.gameTree.currNode
        if  len(curr_node.currPlayer.pieces) ==0 and len(curr_node.oppPlayer.pieces) !=0:
            winner = curr_node.oppPlayer.playerId


        elif len(curr_node.currPlayer.pieces) !=0 and len(curr_node.oppPlayer.pieces) ==0:
            winner = curr_node.currPlayer.playerId

        return winner

    def play(self):

        t0 = timeit.default_timer()

        while timeit.default_timer() < t0 + 5:

            current = self.gameTree.currNode
            while True:

                if current.gameStats.s == 0:
                    winner = current.simulate()

                    if winner != 0:
                        current.updateStats(winner)
                    break

                else:
                    x = current.nextBestMove()
                    if isinstance(x,int):
                        current.updateStats(x)
                        break
                    else:
                        current = x



        x = self.gameTree.nextBestPlay()
        if isinstance(x,int):
            self.status = x
            print("No more plays")
        else:
            self.gameTree.currNode = x

        self.gameTree.currNode.printBoard()
        if self.status == 0:
            self.status = self.getStatus()

class Player:

    def updateKings(self):

        if self.playerId == 1:
            for piece in self.pieces:
                x,y = piece
                if x == 7:
                    self.isKing[self.pieces.index(piece)] = 1
        else:
            for piece in self.pieces:
                x,y = piece
                if x == 0:
                    self.isKing[self.pieces.index(piece)] = 1

    def __init__(self,playerId):
        self.playerId = playerId
        self.pieces = []
        self.isKing = []

        self.isKing.append(0)
        self.isKing.append(0)
        self.isKing.append(0)
        self.isKing.append(0)
        self.isKing.append(0)
        self.isKing.append(0)
        self.isKing.append(0)
        self.isKing.append(0)
        self.isKing.append(0)
        self.isKing.append(0)
        self.isKing.append(0)
        self.isKing.append(0)

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
