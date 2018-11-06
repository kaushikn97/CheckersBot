from classes import *

def get_coord(coord):
    print(len(coord))
    if len(coord)!=2 :
        print("Invalid position.")
        return -1
    
    x = coord[0]
    y = coord[1]
    if ord(x)>64:
        print(ord(x)-65 , int(y)-1)
        return ord(x)-65 , int(y)-1
    
    else:
        print(ord(x)-97 , int(y)-1)
        return ord(x)-97 , int(y)-1
    

def main():
    game = Game()

    while game.status == 0:
        
        print("Red's turn\n\n")
        
        game.play()
        
        if game.status != 0:
            break
        
        while True:
            
            print("\n"),
            if len(game.gameTree.currNode.nextMoves) == 0:
                moves = game.gameTree.currNode.nextMoves
            else:
                moves = game.gameTree.currNode.allPossibleMoves()
                
            if len(moves) == 0:
                print("You have run out of moves.")
                game.status = 1
                break
            
            print "Blue's turn"
            print("\n"),
            print "Enter coordinates of the piece to move:"
            curr = raw_input()
            piece = get_coord(curr)
            if piece == -1 :
                continue
            print "Enter coordinates of the place to move:"
            move_to = raw_input()
            move_loc = get_coord(move_to)
            if move_loc == -1 :
                continue
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
