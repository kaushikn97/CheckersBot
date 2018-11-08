import numpy
import math
import timeit
from random import shuffle
import copy
from termcolor import colored

sim_time = 5

def in_bound(x,y):
    if x < 8 and x >= 0 and y >= 0 and y < 8 :
        return True
    else:
        return False
    
def find(x,y,pieces):
    
    for piece in pieces:
        x_loc,y_loc,isKing = piece
        if x==x_loc and y==y_loc:
            return True
    
    return False

def remove(x,y,pieces):
    
    for piece in pieces:
        x_loc,y_loc,isKing = piece
        if x == x_loc and y == y_loc:
            pieces.remove((x,y,isKing))
            return pieces

# current player is the player who will play the next move
# stats of player 1 are stores
class Stats:

    def __init__(self,parentSimCount):

        self.w = 0.0
        self.s = 0.0
        self.c = 0.5
        self.sp = parentSimCount

    def ucb(self):

        if self.s == 0:
            return 1000.0
        else:
            return (self.w/self.s) + (self.c*math.sqrt(math.log(self.sp + 1)/self.s))

    def probability(self):

        if self.s == 0.0:
            return 0.0
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

        print("Board:\n")
        index = 0
        for piece in self.currPlayer.pieces:
            x,y,isKing = piece
            loc = x,y
            currBoard[loc] = self.currPlayer.playerId
            currKings[loc] = isKing
            index = index + 1
        index = 0
        for piece in self.oppPlayer.pieces:
            x,y,isKing = piece
            loc = x,y
            currBoard[loc] = self.oppPlayer.playerId
            currKings[loc] = isKing
            index = index + 1
        print("   "),
        for i in range(1,9):
            print(i),

        print("\n")


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

        if self.currPlayer.playerId == 1:
            print("\n" + colored("Red","red") + " pieces remaining: " + str(len(self.currPlayer.pieces)))
            print(colored("Blue","cyan") + " pieces remaining: " + str(len(self.oppPlayer.pieces)))
        else:
            print("\n" + colored("Red","red") + " pieces remaining: " + str(len(self.oppPlayer.pieces)))
            print(colored("Blue","cyan") + " pieces remaining: " + str(len(self.currPlayer.pieces)))


    def allPossibleMoves(self):
        moves = []
        pieces = self.currPlayer.pieces
        oppPieces = self.oppPlayer.pieces
        #isKing = self.currPlayer.isKing

        for piece in pieces:
            x,y,isKing = piece
            #piece_index = pieces.index(piece)
           
            if in_bound(x+1,y+1) and (not find(x+1,y+1,pieces)) and (not find(x+1,y+1,oppPieces)) and (self.currPlayer.playerId == 1 or isKing == 1):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces = remove(x,y,temp_player.pieces)
               temp_player.pieces.append((x+1,y+1,isKing))
               if isKing == 0:
                   temp_player.updateKings()
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)

            if in_bound(x-1,y-1) and (not find(x-1,y-1,pieces)) and (not find(x-1,y-1,oppPieces)) and (self.currPlayer.playerId == 2 or isKing == 1):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces = remove(x,y,temp_player.pieces)
               temp_player.pieces.append((x-1,y-1,isKing))
               if isKing == 0:
                   temp_player.updateKings()
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)

            if in_bound(x+1,y-1) and (not find(x+1,y-1,pieces)) and (not find(x+1,y-1,oppPieces)) and (self.currPlayer.playerId == 1 or isKing == 1):


               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces = remove(x,y,temp_player.pieces)
               temp_player.pieces.append((x+1,y-1,isKing))
               if isKing == 0:
                   temp_player.updateKings()
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)

            if in_bound(x-1,y+1) and (not find(x-1,y+1,pieces)) and (not find(x-1,y+1,oppPieces)) and (self.currPlayer.playerId == 2 or isKing == 1):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces = remove(x,y,temp_player.pieces)
               temp_player.pieces.append((x-1,y+1,isKing))
               if isKing == 0:
                   temp_player.updateKings()
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)

            if in_bound(x+2,y+2) and (find(x+1,y+1,oppPieces)) and (not find(x+2,y+2,pieces)) and (not find(x+2,y+2,oppPieces)) and (self.currPlayer.playerId == 1 or isKing == 1):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces = remove(x,y,temp_player.pieces)
               temp_player.pieces.append((x+2,y+2,isKing))
               #temp_opponent.isKing.pop(temp_opponent.pieces.index((x+1,y+1)))
               temp_opponent.pieces = remove(x+1,y+1,temp_opponent.pieces)
               if isKing == 0:
                   temp_player.updateKings()
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)


            if in_bound(x-2,y-2) and (find(x-1,y-1,oppPieces)) and (not find(x-2,y-2,pieces)) and (not find(x-2,y-2,oppPieces)) and (self.currPlayer.playerId == 2 or isKing == 1):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces = remove(x,y,temp_player.pieces)
               temp_player.pieces.append((x-2,y-2,isKing))
               #temp_opponent.isKing.pop(temp_opponent.pieces.index((x-1,y-1)))
               temp_opponent.pieces = remove(x-1,y-1,temp_opponent.pieces)
               if isKing == 0:
                   temp_player.updateKings()
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)

            if in_bound(x-2,y+2) and (find(x-1,y+1,oppPieces)) and (not find(x-2,y+2,pieces)) and (not find(x-2,y+2,oppPieces)) and (self.currPlayer.playerId == 2 or isKing == 1):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces = remove(x,y,temp_player.pieces)
               temp_player.pieces.append((x-2,y+2,isKing))
               #temp_opponent.isKing.pop(temp_opponent.pieces.index((x-1,y+1)))
               temp_opponent.pieces = remove(x-1,y+1,temp_opponent.pieces)
               if isKing == 0:
                   temp_player.updateKings()
               
               new_node = Node(temp_opponent,temp_player,self,self.gameStats.sp)
               moves.append(new_node)

            if in_bound(x+2,y-2) and (find(x+1,y-1,oppPieces)) and (not find(x+2,y-2,pieces)) and (not find(x+2,y-2,oppPieces)) and (self.currPlayer.playerId == 1 or isKing == 1):

               temp_player = copy.deepcopy(self.currPlayer)
               temp_opponent = copy.deepcopy(self.oppPlayer)
               temp_player.pieces = remove(x,y,temp_player.pieces)
               temp_player.pieces.append((x+2,y-2,isKing))
               #temp_opponent.isKing.pop(temp_opponent.pieces.index((x+1,y-1)))
               temp_opponent.pieces = remove(x+1,y-1,temp_opponent.pieces)
               if isKing == 0:
                   temp_player.updateKings()
               
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
        curr_pieces = self.currPlayer.pieces
        opp_pieces = self.oppPlayer.pieces
        winner = 0
        start_time = timeit.default_timer()
        while True:

            if  len(curr_pieces) ==0 and len(opp_pieces) !=0:
                winner = curr_node.oppPlayer.playerId
                break

            elif len(curr_pieces) !=0 and len(opp_pieces) ==0:
                winner = curr_node.currPlayer.playerId
                break

            moves = curr_node.allPossibleMoves()
            if len(moves) == 0:
                winner = curr_node.oppPlayer.playerId
                break
            
            shuffle(moves)
            curr_node = moves[0]
            

        return winner

    def nextBestMove(self):

        #print "Finding next best move"
        if len(self.nextMoves) == 0:
            self.nextMoves = self.allPossibleMoves()
        max_ucb = -1
        if len(self.nextMoves) == 0:
            return self.oppPlayer.playerId
        #print "length of nextmove:", len(self.nextMoves)
        for node in self.nextMoves:
            if node.gameStats.ucb()>max_ucb:
                bestNode = node
                max_ucb = node.gameStats.ucb()

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
            self.currNode.nextMoves = self.currNode.allPossibleMoves()
        max_prob= -1
        max_list = []
        #min_prob = 5000

        if len(self.currNode.nextMoves) == 0:
            return self.currNode.oppPlayer.playerId

        # if self.currNode.oppPlayer.playerId == 2 :
        #     shuffle(self.currNode.nextMoves)
        #     return self.currNode.nextMoves[0]

        for node in self.currNode.nextMoves:
            if node.gameStats.probability()>max_prob:
                bestPlay = node
                max_prob = node.gameStats.probability()
            """if node.gameStats.probability()<min_prob:
                worstPlay = node"""

        if bestPlay.gameStats.probability() == 0.0:
            for node in self.currNode.nextMoves:
                if node.gameStats.probability() == 0.0:
                    max_list.append(node)
                    
        if len(max_list) != 0:
            shuffle(max_list)
            bestPlay = max_list[0]
            
        """print self.currNode.gameStats.w
        print self.currNode.gameStats.s
            
        for node in self.currNode.nextMoves:
            print node.currPlayer.pieces
            print node.oppPlayer.pieces
            print node.gameStats.w
            print node.gameStats.s
            print node.gameStats.ucb()"""
            
            
        return bestPlay

        

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
        
        """if self.gameTree.currNode.currPlayer.playerId == 2:
            moves = []
            if len(self.gameTree.currNode.nextMoves) ==0:
                moves = self.gameTree.currNode.allPossibleMoves()
            else:
                moves = self.gameTree.currNode.nextMoves
                
            shuffle(moves)
            self.gameTree.currNode = moves[0]
            return"""

        t0 = timeit.default_timer()
        counter = 10
        while counter > 0:

            current = self.gameTree.currNode
            while True:
                
                if (len(current.currPlayer.pieces)==0 and len(current.oppPlayer.pieces)!=0) or (len(current.currPlayer.pieces)!=0 and len(current.oppPlayer.pieces)==0) or len(current.nextMoves)==0:
                    counter-=1
                    break

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
                counter-=1

        x = self.gameTree.nextBestPlay()
        if isinstance(x,int):
            self.status = x
            print("Computer has run out of moves.")
        else:
            self.gameTree.currNode = x

        #self.gameTree.currNode.printBoard()
        if self.status == 0:
            self.status = self.getStatus()


    def userPlay(self,piece_loc,move_loc):
        
        
        moves = []

        x,y = piece_loc
        X,Y = move_loc
        
        curr_node = copy.deepcopy(self.gameTree.currNode)

        if (not in_bound(x,y)) or (not in_bound(X,Y) or (not find(x,y,curr_node.currPlayer.pieces))):
            
            print "yes"
            return -1
        
        for piece in self.gameTree.currNode.currPlayer.pieces:
            piece_x,piece_y,isKing = piece
            if x==piece_x and  y==piece_y:
                break

        curr_node.currPlayer.pieces = remove(x,y,curr_node.currPlayer.pieces)
        curr_node.currPlayer.pieces.append((X,Y,isKing))


        if X == x-2 and Y == y+2 and (find(x-1,y+1,curr_node.oppPlayer.pieces)):
            curr_node.oppPlayer.pieces = remove(x-1,y+1,curr_node.oppPlayer.pieces)

        elif X == x-2 and Y == y-2 and (find(x-1,y-1,curr_node.oppPlayer.pieces)):
            curr_node.oppPlayer.pieces = remove(x-1,y-1,curr_node.oppPlayer.pieces)
            
        elif X == x+2 and Y == y+2 and (find(x+1,y+1,curr_node.oppPlayer.pieces)):
            curr_node.oppPlayer.pieces = remove(x+1,y+1,curr_node.oppPlayer.pieces)
            
        elif X == x+2 and Y == y-2 and (find(x+1,y-1,curr_node.oppPlayer.pieces)):
            curr_node.oppPlayer.pieces = remove(x+1,y-1,curr_node.oppPlayer.pieces)
            
        if isKing == 0:
            curr_node.currPlayer.updateKings()

        if len(self.gameTree.currNode.nextMoves) != 0:
            moves = self.gameTree.currNode.nextMoves
        else:
            moves = self.gameTree.currNode.allPossibleMoves()
            

        if len(moves) == 0:
            self.status = 1
            print "in user play"
            print("You have run out of moves.")
            return -1
        

        for move in moves:

            if sorted(move.currPlayer.pieces) == sorted(curr_node.oppPlayer.pieces) and sorted(move.oppPlayer.pieces) == sorted(curr_node.currPlayer.pieces):
                self.gameTree.currNode = move
                return move
            
        if self.status == 0:
            self.status = self.getStatus()

        return -1


class Player:

    def updateKings(self):

        if self.playerId == 1:
           # print "updating 1 kings"
            for piece in self.pieces:
                x,y,isKing = piece
                if x == 7 and isKing == 0:
                        remove(x,y,self.pieces)
                        self.pieces.append((x,y,1))
                       
        if self.playerId == 2:
           # print "updating 2 kings"
            for piece in self.pieces:
                x,y,isKing = piece
                if x == 0 and isKing == 0:
                        remove(x,y,self.pieces)
                        self.pieces.append((x,y,1))
                        
        

    def __init__(self,playerId):
        self.playerId = playerId
        self.pieces = []
       # self.isKing = []

        """self.isKing.append(0)
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
        self.isKing.append(0)"""

        if playerId == 1:
            self.pieces.append((0,1,0))
            self.pieces.append((0,3,0))
            self.pieces.append((0,5,0))
            self.pieces.append((0,7,0))
            self.pieces.append((1,0,0))
            self.pieces.append((1,2,0))
            self.pieces.append((1,4,0))
            self.pieces.append((1,6,0))
            self.pieces.append((2,1,0))
            self.pieces.append((2,3,0))
            self.pieces.append((2,5,0))
            self.pieces.append((2,7,0))
        if playerId == 2:
            self.pieces.append((5,0,0))
            self.pieces.append((5,2,0))
            self.pieces.append((5,4,0))
            self.pieces.append((5,6,0))
            self.pieces.append((6,1,0))
            self.pieces.append((6,3,0))
            self.pieces.append((6,5,0))
            self.pieces.append((6,7,0))
            self.pieces.append((7,0,0))
            self.pieces.append((7,2,0))
            self.pieces.append((7,4,0))
            self.pieces.append((7,6,0))
