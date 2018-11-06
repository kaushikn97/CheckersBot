import numpy
import math
import timeit
from random import shuffle
import copy
from termcolor import colored

sim_time = 1

# Python program to print
# colored text and background
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

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
        currKings = numpy.full((8,8),0)
        if self.currPlayer.playerId == 1:
            print("Red pieces remaining: " + str(len(self.currPlayer.pieces)))
            print("Blue pieces remaining: " + str(len(self.oppPlayer.pieces)))
        else:
            print("Red pieces remaining: " + str(len(self.oppPlayer.pieces)))
            print("Blue pieces remaining: " + str(len(self.currPlayer.pieces)))

        print("\n\n")
        index = 0
        for piece in self.currPlayer.pieces:
            currBoard[piece] = self.currPlayer.playerId
            currKings[piece] = self.currPlayer.isKing[index]
            index = index + 1
        index = 0
        for piece in self.oppPlayer.pieces:
            currBoard[piece] = self.oppPlayer.playerId
            currKings[piece] = self.oppPlayer.isKing[index]
            index = index + 1
        print("   "),
        for i in range(1,9):
            print(i),

        print("\n"),
        print("\n"),

        for i in range(0,8):
            print(chr(65+i)),
            print(" "),
            for j in range(0,8):
                piece = i,j
                if currKings[piece] == 1:
                    print(colored(currBoard[piece],'green')),
                elif currBoard[piece] == 1 :
                    print(colored(currBoard[piece],'red')),
                elif currBoard[piece] == 2 :
                    print(colored(currBoard[piece],'cyan')),
                else:
                    print(currBoard[piece]),
            print("\n"),


    def allPossibleMoves(self):
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

            moves = curr_node.allPossibleMoves()
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
            self.nextMoves = self.allPossibleMoves()
        max_ucb = -1
        if len(self.nextMoves) == 0:
            return self.oppPlayer.playerId
        #print "length of nextmove:", len(self.nextMoves)
        for node in self.nextMoves:
            if node.gameStats.ucb()>max_ucb:
                bestNode = node

        same_moves = []
        if bestNode.gameStats.ucb == 1000:
            for node in self.nextMoves:
                if node.gameStats.ucb == 1000:
                    same_moves.append(node)

        if len(same_moves)!=0:
            shuffle(same_moves)
            bestNode = same_moves[0]

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

        while timeit.default_timer() < t0 + 1:

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
            print("Computer has run out of moves.")
        else:
            self.gameTree.currNode = x

        self.gameTree.currNode.printBoard()
        if self.status == 0:
            self.status = self.getStatus()


    def userPlay(self,piece_loc,move_loc):

        x,y = piece_loc
        X,Y = move_loc
        curr_node = copy.deepcopy(self.gameTree.currNode)

        if (not in_bound(x,y)) or (not in_bound(X,Y) or (piece_loc not in curr_node.currPlayer.pieces)):
            return -1

        curr_node.currPlayer.pieces.remove((x,y))
        curr_node.currPlayer.pieces.append((X,Y))


        if X == x-2 and Y == y+2 and ((x-1,y+1) in curr_node.oppPlayer.pieces):
            curr_node.oppPlayer.pieces.remove((x-1,y+1))

        elif X == x-2 and Y == y-2 and ((x-1,y-1) in curr_node.oppPlayer.pieces):
            curr_node.oppPlayer.pieces.remove((x-1,y-1))

        elif X == x+2 and Y == y+2 and ((x+1,y+1) in curr_node.oppPlayer.pieces):
            curr_node.oppPlayer.pieces.remove((x+1,y+1))

        elif X == x+2 and Y == y-2 and ((x+1,y-1) in curr_node.oppPlayer.pieces):
            curr_node.oppPlayer.pieces.remove((x+1,y-1))

        """print sorted(curr_node.currPlayer.pieces)
        print("\n"),
        print sorted(curr_node.oppPlayer.pieces)"""

        if len(self.gameTree.currNode.nextMoves) == 0:
            moves = self.gameTree.currNode.nextMoves
        else:
            moves = self.gameTree.currNode.allPossibleMoves()

        if len(moves) == 0:
            self.status = 1
            print("You have run out of moves.")
            return -1

        for move in moves:

            """print(sorted(move.currPlayer.pieces))
            print(sorted(move.oppPlayer.pieces))
            print("\n"),"""

            if sorted(move.currPlayer.pieces) == sorted(curr_node.oppPlayer.pieces) and sorted(move.oppPlayer.pieces) == sorted(curr_node.currPlayer.pieces):
                self.gameTree.currNode = move
                return move

        return -1


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
