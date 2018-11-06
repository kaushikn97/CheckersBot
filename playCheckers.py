from classes import *

def main():
    game = Game()

    while game.status == 0:
        
        game.play()
        
        while True:
            
            print("\n"),
        #game.printBoard()

        #game.printBoard()
            print "User's turn"
            print("\n"),
            print "Enter X-coordinate of the piece to move:"
            curr_x = input()
            print "Enter Y-coordinate of the piece to move:"
            curr_y = input()
            piece = curr_x,curr_y
            print "Enter X-coordinate of the place to move:"
            move_x = input()
            print "Enter Y-coordinate of the place to move:"
            move_y = input()
            move_loc = move_x,move_y
            
            move = game.userPlay(piece,move_loc)
            
            if game.status != 0:
                break
            
            if isinstance(move,int):
                print "Invalid move!!"
                
            else:
                break
        print("\n"),
        game.gameTree.currNode.printBoard()
        print("\n"),
        

    print("Player " + str(game.status) + "wins")

if __name__ == '__main__':
    main()
