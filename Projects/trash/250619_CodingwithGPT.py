from tkinter import *
import csv
import time

#---------- DATA CLASSES ----------

class Letter:
    def init(self, letterID, recipientID, day):
        self.letterID = letterID
        self.recipientID = recipientID
        self.day = int(day)
        self.postedID = ""
        self.isMailed = False

    def mail(self, postedID):
        self.postedID = postedID
        self.isMailed = True

class Mailbox:
    def init(self, boxID, address, color="white"):
        self.boxID = boxID
        self.address = address
        self.color = color
        self.hasMail = False
        self.containing = []

    def receive_mail(self, letter):
        self.containing.append(letter)
        self.hasMail = True

#---------- GAME CONTROLLER ----------

class Game:
    def init(self, root):
        self.root = root
        self.root.title("Mail Poster")
        self.root.geometry("600x600")

    # Game state
        self.currentDay = 1
        self.score = 0
        self.postedLetters = 0
        self.wrongDeliveries = 0
        self.dayDuration = 20
        self.dayStartTime = 0
        self.isGameRunning = False

    # Data
        self.all_letters = self.load_letters("letters.csv")
        self.mailboxes = self.load_mailboxes("mailboxes.csv")
        self.letters_today = []

    # UI Elements
        self.timerLabel = Label(root, text="Press Start to begin", font=("Arial", 16))
        self.timerLabel.pack(pady=10)

        self.scoreLabel = Label(root, text="Score: 0", font=("Arial", 12), fg="green")
        self.scoreLabel.pack()

        self.letterInfoVar = StringVar(value="No letters yet.")
        self.letterLabel = Label(root, textvariable=self.letterInfoVar, font=("Arial", 14), fg="purple")
        self.letterLabel.pack(pady=10)

        self.start_button = Button(root, text="Start Day", command=self.start_day, font=("Arial", 14))
        self.start_button.pack(pady=10)

        self.mailbox_buttons = []

    def load_letters(self, filename):
        letters = []
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    letters.append(Letter(row['LetterID'], row['RecipientID'], row['Day']))
        except FileNotFoundError:
            print(f"Error: Could not find {filename}")
        return letters

    def load_mailboxes(self, filename):
        mailboxes = []
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    mailboxes.append(Mailbox(row['BoxID'], row['Address'], row.get('Color', 'white')))
        except FileNotFoundError:
            print(f"Error: Could not find {filename}")
        return mailboxes

    def start_day(self):
        if not self.isGameRunning:
            self.isGameRunning = True
            self.dayStartTime = time.time()
            self.letters_today = [l for l in self.all_letters if l.day == self.currentDay]
            self.current_letter_index = 0
            self.update_letter_ui()
            self.create_mailbox_buttons()
            self.update_timer()

    def update_letter_ui(self):
        if self.current_letter_index < len(self.letters_today):
            letter = self.letters_today[self.current_letter_index]
            self.letterInfoVar.set(f"Deliver letter for {letter.recipientID}")
        else:
            self.letterInfoVar.set("All letters delivered.")

    def create_mailbox_buttons(self):
        for btn in self.mailbox_buttons:
            btn.destroy()
        self.mailbox_buttons.clear()

        for mailbox in self.mailboxes:
            btn = Button(self.root, text=mailbox.address, font=("Arial", 12),
                        bg=mailbox.color, command=lambda mb=mailbox: self.post_letter(mb))
            btn.pack(pady=2)
            self.mailbox_buttons.append(btn)

    def post_letter(self, mailbox):
        if self.current_letter_index >= len(self.letters_today):
            return

        letter = self.letters_today[self.current_letter_index]
        letter.mail(mailbox.boxID)
        mailbox.receive_mail(letter)

        if letter.recipientID == mailbox.boxID:
            self.score += 1
        else:
            self.wrongDeliveries += 1

        self.postedLetters += 1
        self.scoreLabel.config(text=f"Score: {self.score}")

        self.current_letter_index += 1
        self.update_letter_ui()

    def update_timer(self):
        if self.isGameRunning:
            elapsed = time.time() - self.dayStartTime
            remaining = round(max(0, self.dayDuration - elapsed), 1)

            if remaining > 0:
                self.timerLabel.config(text=f"Time remaining: {remaining:.1f} seconds")
                self.root.after(100, self.update_timer)
            else:
                self.end_day()

    def end_day(self):
        self.isGameRunning = False
        self.timerLabel.config(text="Day Over!")
        self.letterInfoVar.set(f"Posted {self.postedLetters} letters | Score: {self.score}")

#---------- MAIN TKINTER LOOP ----------

if __name__ == "main":
    root = Tk()
    game = Game(root)
    root.mainloop()