from classes import *
from termcolor import colored

def get_coord(coord):
    if len(coord)!=2 :
        print(colored("\nInvalid position.","yellow"))
        return -1
    if not (ord(coord[1]) in range(49,57)) :
        print(colored("\nInvalid position.","yellow"))
        return -1
    if not ((ord(coord[0]) in range(97,105)) or (ord(coord[0]) in range(65,73))):
        print(colored("\nInvalid position.","yellow"))
        return -1

    x = coord[0]
    y = coord[1]

    if ord(x)<97:
        return ord(x)-65 , int(y)-1
    else:
        return ord(x)-97 , int(y)-1


def main():
    game = Game()

    print("\n\nWelcome to the Checkers game. You control the " + colored("blue","cyan") + " pieces. The computer will control the  " + colored("red","red") + " pieces. Red plays first.\n")
    game.gameTree.currNode.printBoard()
    print game.gameTree.currNode.currPlayer.playerId
    raw_input("\nPress any enter to start the game.")

    while game.status == 0:
        print("\n*****************************************************************\n")

        print(colored("Red","red") + " is thinking...\n")
        red_moves = []
        if len(game.gameTree.currNode.nextMoves)!=0:
            red_moves = game.gameTree.currNode.nextMoves
        else:
            red_moves = game.gameTree.currNode.allPossibleMoves()
            
        if len(red_moves)==0 or len(game.gameTree.currNode.currPlayer.pieces)==0:
            game.status = 2
            break
            
        game.play()
        print(colored("Red","red") + " has played.\n")

        print("*****************************************************************")
        if game.status != 0:
            break

        while True:

            print("\n"),
            moves = []
            #print game.gameTree.currNode.currPlayer.playerId
            if len(game.gameTree.currNode.nextMoves) != 0:
                moves = game.gameTree.currNode.nextMoves
            else:
                moves = game.gameTree.currNode.allPossibleMoves()
                

            if len(moves) == 0:
                print("You have run out of moves.")
                game.status = 1
                break

            game.gameTree.currNode.printBoard()

            if game.status!=0:
                break

            print("\n" + colored("Blue's","cyan") + " turn")
            piece = get_coord(raw_input("Enter coordinates of the piece to move:"))
            if piece == -1 :
                continue
            move_loc = get_coord(raw_input("Enter coordinates of the place to move:"))
            if move_loc == -1 :
                continue
            print("")
            move = game.userPlay(piece,move_loc)
            
            #game.play()

            if game.status != 0:
                break

            """if isinstance(move,int):
                print(colored("Invalid move. Please try again.","yellow"))

            else:
                break"""
            break


        game.gameTree.currNode.printBoard()

    if str(game.status) == "1" :
        print(colored("\nRed","red") + " wins.")
    elif str(game.status) == "2" :
        print(colored("\nBlue","cyan") + " wins.")
    else:
        print("The game has ended in a draw.")
        
    game.gameTree.currNode.printBoard()

if __name__ == '__main__':
    main()
