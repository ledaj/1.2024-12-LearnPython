from tkinter import *
from trash.reorg.GUIsh.reorg.GUI import GameUI
from trash.reorg.Models import load_letters, load_mailboxes, letters_path, mailboxes_path

class GameController:
    def __init__(self):
        # GAME STATE
        self.root = Tk()
        self.letters = load_letters("letters.csv")
        self.mailboxes = load_mailboxes("mailboxes.csv")
        self.current_day = 1
        self.current_letter_index = 0
        self.timer = Timer(20)
        self.score = 0
        self.wrong_deliveries = 0
        self.missed_letters = []
        self.ui = GameUI(self.root, self)