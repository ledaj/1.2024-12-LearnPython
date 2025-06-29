from tkinter import *
from game_controller import GameController

def main():
    root = Tk()
    app = GameController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
