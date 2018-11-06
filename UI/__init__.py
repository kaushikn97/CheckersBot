from Tkinter import Tk
from CheckersBoard import CheckersBoard
from CheckersBoardUI import CheckersBoardUI


def main():
    root = Tk()
    checkers_board_UI = CheckersBoardUI(root)
    root.mainloop()


main()
