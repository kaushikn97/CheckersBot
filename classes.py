"""
Classes.py
========================================================

This file includes all the main classes for the Classes.py
including Game, Player, Node, Tree and Stats

"""
import numpy
import math
import timeit
from random import shuffle
import copy
from termcolor import colored

# current player is the player who will play the next move
# stats of player 1 are stores


def probability(node):
    """
    This fuction reurns to probability of winning starting from the given node as estimated by previous simulations.

    """

    if node.gameStats.s == 0.0:
        return 0.0
    else:
        return (node.gameStats.w / node.gameStats.s)


def ucb(node):
    """
    This function descirbes the policy using which the tree will expand. It implements a modified version of UCB giving the player a more agressive playing style.

    """

    if node.gameStats.s == 0:
        return 1000.0
    else:

        kingsCount = 0.0
        for piece in node.oppPlayer.pieces:
            x, y, isKing = piece
            if isKing == 1:
                kingsCount += 1

        return (node.gameStats.w / node.gameStats.s) + (math.sqrt(math.log(node.parentNode.gameStats.s + 1) / node.gameStats.s)) + kingsCount + node.killedOppPlayer


def in_bound(x, y):
    """This function checks if the piece lies in the bounds of the board or not
        Here the size of the board is 8 X 8.

    """
    if x < 8 and x >= 0 and y >= 0 and y < 8:
        return True
    else:
        return False


def find(x, y, pieces):
    """This function returns whether the current position hold a piece or not from the pieces array sent as argument

    """
    for piece in pieces:
        x_loc, y_loc, isKing = piece
        if x == x_loc and y == y_loc:
            return True

    return False


def remove(x, y, pieces):
    """Function removes a particular piece from the given coordinates if present

    """
    for piece in pieces:
        x_loc, y_loc, isKing = piece
        if x == x_loc and y == y_loc:
            pieces.remove((x, y, isKing))
            return pieces


class Stats:
    """The class contains essential statistic based functions -- Initializes the number of simulations as zero, number of Wins as zero and exploitation parameter as 0.5.

    """

    def __init__(self, parentSimCount):

        self.w = 0.0
        self.s = 0.0
        self.c = 0.5
        self.sp = parentSimCount


class Node:
    """The node class which stores the positions of players' pieces and the nextMoves available.
    It also houses important functions for simulating the game, finding all possible moves, finding the next best move,  and updating the tree.

    """

    def __init__(self, player, opponent, parent=None, parentSimCount=0, killed=0):
        self.visited = False
        self.gameStats = Stats(parentSimCount)
        self.killedOppPlayer = killed
        self.oppPlayer = opponent
        self.currPlayer = player
        self.nextMoves = []
        self.parentNode = parent

    def printBoard(self):
        """Print the board i.e. prints the positions of the player and the opposition and also returns the pieces remaining

        """
        currBoard = numpy.full((8, 8), 0)
        currKings = numpy.full((8, 8), 0)

        print("\tBoard:\n")
        index = 0
        for piece in self.currPlayer.pieces:
            x, y, isKing = piece
            loc = x, y
            currBoard[loc] = self.currPlayer.playerId
            currKings[loc] = isKing
            index = index + 1
        index = 0
        for piece in self.oppPlayer.pieces:
            x, y, isKing = piece
            loc = x, y
            currBoard[loc] = self.oppPlayer.playerId
            currKings[loc] = isKing
            index = index + 1
        print("\t   "),
        for i in range(1, 9):
            print(i),

        print("\n")

        for i in range(0, 8):
            print("\t"),
            print(chr(65 + i)),
            print(" "),
            for j in range(0, 8):
                piece = i, j
                if currKings[piece] == 1:
                    if currBoard[piece] == 1:
                        print(colored(u'\u2776', 'green')),
                    else:
                        print(colored(u'\u2777', 'green')),
                elif currBoard[piece] == 1:
                    print(colored(u'\u2776', 'red')),
                elif currBoard[piece] == 2:
                    print(colored(u'\u2777', 'blue')),
                else:
                    print(u'\u25cc'),
            print("\n"),

        if self.currPlayer.playerId == 1:
            print("\n\t" + colored("Red", "red") +
                  " pieces remaining: " + str(len(self.currPlayer.pieces)))
            print("\t" + colored("Blue", "blue") +
                  " pieces remaining: " + str(len(self.oppPlayer.pieces)))
        else:
            print("\n\t" + colored("Red", "red") +
                  " pieces remaining: " + str(len(self.oppPlayer.pieces)))
            print("\t" + colored("Blue", "blue") +
                  " pieces remaining: " + str(len(self.currPlayer.pieces)))

    def allPossibleMoves(self):
        """The function returns all the possible moves by checking the current game state.

        """

        moves = []
        pieces = self.currPlayer.pieces
        oppPieces = self.oppPlayer.pieces

        for piece in pieces:
            x, y, isKing = piece

            if in_bound(x + 1, y + 1) and (not find(x + 1, y + 1, pieces)) and (not find(x + 1, y + 1, oppPieces)) and (self.currPlayer.playerId == 1 or isKing == 1):

                temp_player = copy.deepcopy(self.currPlayer)
                temp_opponent = copy.deepcopy(self.oppPlayer)
                temp_player.pieces = remove(x, y, temp_player.pieces)
                temp_player.pieces.append((x + 1, y + 1, isKing))
                if isKing == 0:
                    temp_player.updateKings()
                new_node = Node(temp_opponent, temp_player,
                                self, self.gameStats.sp)
                moves.append(new_node)

            if in_bound(x - 1, y - 1) and (not find(x - 1, y - 1, pieces)) and (not find(x - 1, y - 1, oppPieces)) and (self.currPlayer.playerId == 2 or isKing == 1):

                temp_player = copy.deepcopy(self.currPlayer)
                temp_opponent = copy.deepcopy(self.oppPlayer)
                temp_player.pieces = remove(x, y, temp_player.pieces)
                temp_player.pieces.append((x - 1, y - 1, isKing))
                if isKing == 0:
                    temp_player.updateKings()
                new_node = Node(temp_opponent, temp_player,
                                self, self.gameStats.sp)
                moves.append(new_node)

            if in_bound(x + 1, y - 1) and (not find(x + 1, y - 1, pieces)) and (not find(x + 1, y - 1, oppPieces)) and (self.currPlayer.playerId == 1 or isKing == 1):

                temp_player = copy.deepcopy(self.currPlayer)
                temp_opponent = copy.deepcopy(self.oppPlayer)
                temp_player.pieces = remove(x, y, temp_player.pieces)
                temp_player.pieces.append((x + 1, y - 1, isKing))
                if isKing == 0:
                    temp_player.updateKings()
                new_node = Node(temp_opponent, temp_player,
                                self, self.gameStats.sp)
                moves.append(new_node)

            if in_bound(x - 1, y + 1) and (not find(x - 1, y + 1, pieces)) and (not find(x - 1, y + 1, oppPieces)) and (self.currPlayer.playerId == 2 or isKing == 1):

                temp_player = copy.deepcopy(self.currPlayer)
                temp_opponent = copy.deepcopy(self.oppPlayer)
                temp_player.pieces = remove(x, y, temp_player.pieces)
                temp_player.pieces.append((x - 1, y + 1, isKing))
                if isKing == 0:
                    temp_player.updateKings()
                new_node = Node(temp_opponent, temp_player,
                                self, self.gameStats.sp)
                moves.append(new_node)

            if in_bound(x + 2, y + 2) and (find(x + 1, y + 1, oppPieces)) and (not find(x + 2, y + 2, pieces)) and (not find(x + 2, y + 2, oppPieces)) and (self.currPlayer.playerId == 1 or isKing == 1):

                temp_player = copy.deepcopy(self.currPlayer)
                temp_opponent = copy.deepcopy(self.oppPlayer)
                temp_player.pieces = remove(x, y, temp_player.pieces)
                temp_player.pieces.append((x + 2, y + 2, isKing))
                temp_opponent.pieces = remove(
                    x + 1, y + 1, temp_opponent.pieces)
                if isKing == 0:
                    temp_player.updateKings()
                new_node = Node(temp_opponent, temp_player,
                                self, self.gameStats.sp)
                moves.append(new_node)

            if in_bound(x - 2, y - 2) and (find(x - 1, y - 1, oppPieces)) and (not find(x - 2, y - 2, pieces)) and (not find(x - 2, y - 2, oppPieces)) and (self.currPlayer.playerId == 2 or isKing == 1):

                temp_player = copy.deepcopy(self.currPlayer)
                temp_opponent = copy.deepcopy(self.oppPlayer)
                temp_player.pieces = remove(x, y, temp_player.pieces)
                temp_player.pieces.append((x - 2, y - 2, isKing))
                temp_opponent.pieces = remove(
                    x - 1, y - 1, temp_opponent.pieces)
                if isKing == 0:
                    temp_player.updateKings()
                new_node = Node(temp_opponent, temp_player,
                                self, self.gameStats.sp)
                moves.append(new_node)

            if in_bound(x - 2, y + 2) and (find(x - 1, y + 1, oppPieces)) and (not find(x - 2, y + 2, pieces)) and (not find(x - 2, y + 2, oppPieces)) and (self.currPlayer.playerId == 2 or isKing == 1):

                temp_player = copy.deepcopy(self.currPlayer)
                temp_opponent = copy.deepcopy(self.oppPlayer)
                temp_player.pieces = remove(x, y, temp_player.pieces)
                temp_player.pieces.append((x - 2, y + 2, isKing))
                temp_opponent.pieces = remove(
                    x - 1, y + 1, temp_opponent.pieces)
                if isKing == 0:
                    temp_player.updateKings()

                new_node = Node(temp_opponent, temp_player,
                                self, self.gameStats.sp)
                moves.append(new_node)

            if in_bound(x + 2, y - 2) and (find(x + 1, y - 1, oppPieces)) and (not find(x + 2, y - 2, pieces)) and (not find(x + 2, y - 2, oppPieces)) and (self.currPlayer.playerId == 1 or isKing == 1):

                temp_player = copy.deepcopy(self.currPlayer)
                temp_opponent = copy.deepcopy(self.oppPlayer)
                temp_player.pieces = remove(x, y, temp_player.pieces)
                temp_player.pieces.append((x + 2, y - 2, isKing))
                temp_opponent.pieces = remove(
                    x + 1, y - 1, temp_opponent.pieces)
                if isKing == 0:
                    temp_player.updateKings()

                new_node = Node(temp_opponent, temp_player,
                                self, self.gameStats.sp)
                moves.append(new_node)

        return moves

    def updateStats(self, winner):
        """Based on the game played out updates the  s and w values respectively

        """
        self.gameStats.s = self.gameStats.s + 1

        if(winner == 1):
            self.gameStats.w = self.gameStats.w + 1

        if(self.parentNode == None):
            return
        else:
            self.parentNode.updateStats(winner)
            return

    def simulate(self):
        """Runs a Monte Carlo Simulation until a player wins. In the loop all the possible moves are caluated.

        """

        curr_node = self
        curr_pieces = self.currPlayer.pieces
        opp_pieces = self.oppPlayer.pieces
        winner = 0
        start_time = timeit.default_timer()
        while True:

            if len(curr_pieces) == 0 and len(opp_pieces) != 0:
                winner = curr_node.oppPlayer.playerId
                break

            elif len(curr_pieces) != 0 and len(opp_pieces) == 0:
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
        """Finds the next best move to expand the search tree based on the given policy and its acquired statistics.

        """
        # print "Finding next best move"
        if len(self.nextMoves) == 0:
            self.nextMoves = self.allPossibleMoves()
        max_ucb = -1
        if len(self.nextMoves) == 0:
            return self.oppPlayer.playerId
        # print "length of nextmove:", len(self.nextMoves)
        for node in self.nextMoves:
            temp_ucb = ucb(node)
            if temp_ucb > max_ucb:
                bestNode = node
                max_ucb = temp_ucb

        same_moves = []
        if ucb(bestNode) == 1000:
            for node in self.nextMoves:
                if ucb(node) == 1000:
                    same_moves.append(node)

        if len(same_moves) != 0:
            shuffle(same_moves)
            bestNode = same_moves[0]

        return bestNode


class Tree:
    """Tree class which builds the Game tree which has a node consisting of the two players' nodes

    """

    def __init__(self):
        self.root = Node(Player(1), Player(2))
        self.currNode = self.root

    def nextBestPlay(self):
        """Finds the next best play based on the maximum probability value of winning acquired from the current game state

        """

        if len(self.currNode.nextMoves) == 0:
            self.currNode.nextMoves = self.currNode.allPossibleMoves()
        max_prob = -1
        max_list = []
        min_prob = 5000

        if len(self.currNode.nextMoves) == 0:
            return self.currNode.oppPlayer.playerId

        # if self.currNode.oppPlayer.playerId == 2 :
        #     shuffle(self.currNode.nextMoves)
        #     return self.currNode.nextMoves[0]

        for node in self.currNode.nextMoves:
            prob = probability(node)
            if prob > max_prob:
                bestPlay = node
                max_prob = prob
            if probability(node) < min_prob:
                worstPlay = node
                min_prob = probability(node)

        if probability(bestPlay) == 0.0:
            for node in self.currNode.nextMoves:
                if probability(node) == 0.0:
                    max_list.append(node)

        if len(max_list) != 0:
            shuffle(max_list)
            bestPlay = max_list[0]

        # print self.currNode.gameStats.w
        # print self.currNode.gameStats.s

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
        self.difficulty = 1

    def setDifficulty(self, diff):
        """
        Sets the difficulty level at which the computer plays by altering the amount of simulation time given to it to exapnd the tree.

        """
        self.difficulty = diff

    def getStatus(self):
        """
        This function returns current game status.

        """
        winner = 0
        curr_node = self.gameTree.currNode
        if len(curr_node.currPlayer.pieces) == 0 and len(curr_node.oppPlayer.pieces) != 0:
            winner = curr_node.oppPlayer.playerId

        elif len(curr_node.currPlayer.pieces) != 0 and len(curr_node.oppPlayer.pieces) == 0:
            winner = curr_node.currPlayer.playerId

        return winner

    def play(self):
        """The play function informs the AI player that it is its turn to play and decides its move
        """

        """
        Uncomment for playing with non-intelligent agent
        if self.gameTree.currNode.currPlayer.playerId == 2:
            moves = []
            if len(self.gameTree.currNode.nextMoves) == 0:
                moves = self.gameTree.currNode.allPossibleMoves()
            else:
                moves = self.gameTree.currNode.nextMoves

            shuffle(moves)
            self.gameTree.currNode = moves[0]
            return"""

        t0 = timeit.default_timer()
        counter = 100 * self.difficulty
        while timeit.default_timer() < t0 + self.difficulty:

            current = self.gameTree.currNode
            while True:

                if current.gameStats.s == 0:
                    winner = current.simulate()

                    if winner != 0:
                        current.updateStats(winner)
                    break

                else:
                    x = current.nextBestMove()
                    if isinstance(x, int):
                        current.updateStats(x)
                        break
                    else:
                        current = x
                counter -= 1

        x = self.gameTree.nextBestPlay()
        if isinstance(x, int):
            self.status = x
            print("\tComputer has run out of moves.")
        else:
            self.gameTree.currNode = x

        if self.status == 0:
            self.status = self.getStatus()

    def userPlay(self, piece_loc, move_loc):
        """
        Function for validiting the user's move  based on the current game state and implementing the same (make necessary updates)

        """
        moves = []

        x, y = piece_loc
        X, Y = move_loc

        curr_node = copy.deepcopy(self.gameTree.currNode)

        if (not in_bound(x, y)) or (not in_bound(X, Y) or (not find(x, y, curr_node.currPlayer.pieces))):
            return -1

        flag = 0
        for piece in self.gameTree.currNode.currPlayer.pieces:
            piece_x, piece_y, isKing = piece
            if x == piece_x and y == piece_y:
                flag = 1
                break

        if flag == 0:
            return -1

        curr_node.currPlayer.pieces = remove(x, y, curr_node.currPlayer.pieces)
        curr_node.currPlayer.pieces.append((X, Y, isKing))

        if X == x - 2 and Y == y + 2 and (find(x - 1, y + 1, curr_node.oppPlayer.pieces)):
            curr_node.oppPlayer.pieces = remove(
                x - 1, y + 1, curr_node.oppPlayer.pieces)

        elif X == x - 2 and Y == y - 2 and (find(x - 1, y - 1, curr_node.oppPlayer.pieces)):
            curr_node.oppPlayer.pieces = remove(
                x - 1, y - 1, curr_node.oppPlayer.pieces)

        elif X == x + 2 and Y == y + 2 and (find(x + 1, y + 1, curr_node.oppPlayer.pieces)):
            curr_node.oppPlayer.pieces = remove(
                x + 1, y + 1, curr_node.oppPlayer.pieces)

        elif X == x + 2 and Y == y - 2 and (find(x + 1, y - 1, curr_node.oppPlayer.pieces)):
            curr_node.oppPlayer.pieces = remove(
                x + 1, y - 1, curr_node.oppPlayer.pieces)

        if isKing == 0:
            curr_node.currPlayer.updateKings()

        if len(self.gameTree.currNode.nextMoves) != 0:
            moves = self.gameTree.currNode.nextMoves
        else:
            moves = self.gameTree.currNode.allPossibleMoves()

        if len(moves) == 0:
            self.status = 1
            print("\tYou have run out of moves.")
            return -1

        ret = -1
        for move in moves:
            if sorted(move.currPlayer.pieces) == sorted(curr_node.oppPlayer.pieces) and sorted(move.oppPlayer.pieces) == sorted(curr_node.currPlayer.pieces):
                self.gameTree.currNode = move
                ret = move
                break

        if self.status == 0:
            self.status = self.getStatus()

        if self.status == 0:
            self.status = self.getStatus()

        return ret


class Player:
    """The player class stores the type of player and its correspondinig pieces

    """

    def updateKings(self):
        """Checks if piece if any of the pieces have become a king after the current and updates the piece's stautus

        """
        if self.playerId == 1:
            for piece in self.pieces:
                x, y, isKing = piece
                if x == 7 and isKing == 0:
                    remove(x, y, self.pieces)
                    self.pieces.append((x, y, 1))

        if self.playerId == 2:
            for piece in self.pieces:
                x, y, isKing = piece
                if x == 0 and isKing == 0:
                    remove(x, y, self.pieces)
                    self.pieces.append((x, y, 1))

    def __init__(self, playerId):
        self.playerId = playerId
        self.pieces = []

        if playerId == 1:
            self.pieces.append((0, 1, 0))
            self.pieces.append((0, 3, 0))
            self.pieces.append((0, 5, 0))
            self.pieces.append((0, 7, 0))
            self.pieces.append((1, 0, 0))
            self.pieces.append((1, 2, 0))
            self.pieces.append((1, 4, 0))
            self.pieces.append((1, 6, 0))
            self.pieces.append((2, 1, 0))
            self.pieces.append((2, 3, 0))
            self.pieces.append((2, 5, 0))
            self.pieces.append((2, 7, 0))
        if playerId == 2:
            self.pieces.append((5, 0, 0))
            self.pieces.append((5, 2, 0))
            self.pieces.append((5, 4, 0))
            self.pieces.append((5, 6, 0))
            self.pieces.append((6, 1, 0))
            self.pieces.append((6, 3, 0))
            self.pieces.append((6, 5, 0))
            self.pieces.append((6, 7, 0))
            self.pieces.append((7, 0, 0))
            self.pieces.append((7, 2, 0))
            self.pieces.append((7, 4, 0))
            self.pieces.append((7, 6, 0))
