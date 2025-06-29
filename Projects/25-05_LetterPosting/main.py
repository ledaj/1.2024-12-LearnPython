# from utils import test
# test.test_method()
from tkinter import *
from game_controller import controller

def main():
    root = Tk()
    app = controller.GameController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
