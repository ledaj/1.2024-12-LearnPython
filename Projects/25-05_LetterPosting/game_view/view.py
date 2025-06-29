from tkinter import *


class GameView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root

        self.root.title("MailPoster")
        self.root.geometry("800x600")

        self.score_label = Label(root, text="Score: 0", font=("Arial", 16))
        self.score_label.pack(pady=10)

        self.click_button = Button(root, text="Click !", command = self.controller.on_click,font=("Arial", 14))
        self.click_button.pack(pady=5)

        self.reset_button = Button(root, text="Reset", command=self.controller.on_reset)
        self.reset_button.pack(pady=5)

    def update_score(self, score):
        self.score_label.config(text=f"Score: {score}")