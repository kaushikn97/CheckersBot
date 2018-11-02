import numpy
import math

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
        else
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
        else
            return false

    def allPossibleMoves(self):
        moves = []
        pieces = self.currPlayer.pieces
        oppPieces = self.oppPlayer.pieces
        for piece in pieces:
            if self.currPlayer.playerId==1 :
                x,y = piece
                if piece is (-1,-1):
                    continue

                if in_bound(x+1,y+1) and ((x+1,y+1) not in pieces) and ((x+1,y+1) not in oppPieces):
                    moves.append(((x,y),(x+1,y+1)))
                if in_bound(x-1,y+1) and (x-1,y+1) not in pieces:
                    moves.append(((x,y),(x-1,y+1)))
                if in_bound(x+1,y-1) and x+1,y-1 not in pieces:
                    moves.append(((x,y),(x+1,y-1)))
                if in_bound(x-1,y-1) and x-1,y-1 not in pieces:
                    moves.append(((x,y),(x-1,y-1)))

                if (x+1,y+1) in oppPieces and (x+2,y+2 not in pieces) and (x+2,y+2 not in oppPieces):
                    moves.append(((x,y),(x+2,y+2),(x+1,y+1),(-1,-1)))
                if (x-1,y-1) in oppPieces and (x-2,y-2 not in pieces) and (x-2,y-2 not in oppPieces):
                    moves.append(((x,y),(x-2,y-2),(x-1,y-1),(-1,-1)))
                if (x-1,y+1) in oppPieces and (x-2,y+2 not in pieces) and (x-2,y+2 not in oppPieces):
                    moves.append(((x,y),(x-2,y+2),(x-1,y+1),(-1,-1)))
                if (x+1,y-1) in oppPieces and (x+2,y-2 not in pieces) and (x+2,y-2 not in oppPieces):
                    moves.append(((x,y),(x+2,y-2),(x+1,y-1),(-1,-1)))




class Tree:

    def __init__(self):
        self.root = Node(Player(1),Player(2))
        self.currNode = self.root

    def nextBestMove(self):

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
        gameTree.currNode = gameTree.nextBestMove()


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
