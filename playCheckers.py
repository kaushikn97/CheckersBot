from classes import *

def main():
    game = Game()

    while game.status == 0:

        game.play()
        game.printBoard()

        if game.status != 0:
            break

        game.play()
        game.printBoard()

    print("Player " + str(game.status) + "wins")

if __name__ == '__main__':
    main()
