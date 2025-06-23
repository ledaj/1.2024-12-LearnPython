from tkinter import *

class GameUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("LetterPoster")

        # Elements
        self.timer_label = Label(root, text="Press Start to begin", font=("Arial", 16))
        self.timer_label.pack(pady=20)

        self.day_label = Label(root, text=f"Day {self.current_day}", font=("Arial", 12))
        self.day_label.pack()

        self.letter_info_var = StringVar(value="No letters yet.")
        self.letter_label = Label(root, textvariable=self.letter_info_var,font=("Arial", 14), fg="purple")
        self.letter_label.pack(pady=10)

        self.start_button = Button(root, text="Start Day", command=self.start_day, font=("Arial", 14))
        self.start_button.pack(pady=10)

        self.mailbox_buttons = []

        self.screen_label = Label(self.root, text="", font=("Arial", 12))
        self.screen_label.pack()

def create_mailboxes_buttons(self):
    for btn in self.mailbox_buttons:
        btn.destroy()
    self.mailbox_buttons.clear()

    if hasattr(self,'mailbox_frame'):
        self.mailbox_frame.destroy()
    
    self.mailbox_frame = Frame(self.root)
    self.mailbox_frame.pack(pady=10)

    screen_mailboxes = [mb for mb in self.mailboxes if mb.screen == self.current_screen]

    self.key_mapped_buttons.clear()

    for index, mailbox in enumerate(screen_mailboxes):
        btn = Button(self.mailbox_frame, text=mailbox.address, font=("Arial", 12), bg=mailbox.color, command=lambda mb=mailbox, b=index: self.post_letter(mb, b))
        btn.grid(row=0, column=index, padx=10)
        self.mailbox_buttons.append(btn)

    if index == 0:
        self.key_mapped_buttons['q'] = mailbox
    elif index == 1:
        self.key_mapped_buttons['d'] = mailbox
