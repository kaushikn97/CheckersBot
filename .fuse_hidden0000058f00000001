from classes import *

def main():
    game = Game()

    while game.status == 0:

        game.play(1)
        game.printBoard()

        if game.status != 0:
            break

        game.play(2)
        game.printBoard()

    print("Player " + str(game.status) + "wins")

if __name__ == '__main__':
    main()
