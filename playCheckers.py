from classes import *
from termcolor import colored
import webbrowser
import time

def get_coord(coord):

    if len(coord)!=2 :
        print(colored("\n\tInvalid position.","yellow"))
        return -1

    if not (ord(coord[1]) in range(49,57)) :
        print(colored("\n\tInvalid position.","yellow"))
        return -1

    if not ((ord(coord[0]) in range(97,105)) or (ord(coord[0]) in range(65,73))):
        print(colored("\n\tInvalid position.","yellow"))
        return -1

    x = coord[0]
    y = coord[1]

    if ord(x)<97:
        return ord(x)-65 , int(y)-1
    else:
        return ord(x)-97 , int(y)-1


def main():
    game = Game() #Game object initialized

    print("\n\nWelcome to the Checkers game. You control the " + colored("blue","blue") + " pieces. The computer will control the  " + colored("red","red") + " pieces. " + colored("Red","red") + " plays first.\n")
    game.gameTree.currNode.printBoard()

    want_help = raw_input("\n\tDo you want to read the rules of checkers before you start playing? (y/n)")

    if want_help == 'y' or want_help == 'Y':
        webbrowser.open_new("./rules.html")

    time.sleep(1)

    diff = input("\tEnter the difficulty you want the computer to play at (1 to 10): ")

    while diff not in range(1,11):
        diff = input("\tPlease enter valid difficulty level (1 to 10): ")

    game.setDifficulty(diff)

    raw_input("\tPress enter to begin the game.")

    while game.status == 0:
        print("\n\t*****************************************************************\n")

        print("\t" + colored("Red","red") + " is thinking...\n")

        if len(game.gameTree.currNode.nextMoves)!=0:
            red_moves = game.gameTree.currNode.nextMoves
        else:
            red_moves = game.gameTree.currNode.allPossibleMoves()

        if len(red_moves)==0 or len(game.gameTree.currNode.currPlayer.pieces)==0:
            game.status = 2
            break

        game.play()
        print("\t" + colored("Red","red") + " has played.\n")

        print("\t*****************************************************************")
        if game.status != 0:
            break

        while True:

            print("\n"),

            if len(game.gameTree.currNode.nextMoves) != 0:
                moves = game.gameTree.currNode.nextMoves
            else:
                moves = game.gameTree.currNode.allPossibleMoves()


            if len(moves) == 0:
                print("\tYou have run out of moves.")
                game.status = 1
                break

            game.gameTree.currNode.printBoard()

            if game.status!=0:
                break

            print("\n\t" + colored("Blue's","blue") + " turn")

            piece = get_coord(raw_input("\tEnter coordinates of the piece to move:"))

            if piece == -1 :
                continue

            move_loc = get_coord(raw_input("\tEnter coordinates of the place to move:"))

            if move_loc == -1 :
                continue

            print("")

            move = game.userPlay(piece,move_loc)

            if game.status != 0:
                break

            if isinstance(move,int):
                print(colored("\tInvalid move. Please try again.","yellow"))

            else:
                break

            break


        game.gameTree.currNode.printBoard()

    if str(game.status) == "1" :
        print(colored("\n\tRed","red") + " wins.")
    elif str(game.status) == "2" :
        print(colored("\n\tBlue","blue") + " wins.")
    else:
        print("\tThe game has ended in a draw.")

    game.gameTree.currNode.printBoard()

if __name__ == '__main__':
    main()
