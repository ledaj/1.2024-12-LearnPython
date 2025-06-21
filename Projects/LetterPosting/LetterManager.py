from tkinter import *
import csv
import time
import os

"""STORY
You have 2 mailboxes and a stack of letters.
You post the letters one by one to the mailboxes and try to match the addresses. This is your score.
Once you have no mail left, game over.
"""

#---- THERE WAS DATA


##--- LETTERS

class Letter():
    def __init__(self, letterID, recipientID, day):
        self.letterID = letterID
        self.recipientID = recipientID
        self.day = int(day)
        self.postedID = ""
        self.is_mailed = False

    def mail(self, postedID):
        self.postedID = postedID
        self.is_mailed = True

##--- MAILBOXES

class Mailbox():
    def __init__(self, boxID, address, color="white"):
        self.boxID = boxID
        self.address = address
        self.has_mail = False
        self.color = color
        self.containing = []
    
    def receiveMail(self, letter):
        self.containing.append(letter)
        self.has_mail = True

##--- PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

letters_path = os.path.join(BASE_DIR, "Letters.csv")
mailboxes_path = os.path.join(BASE_DIR, "Mailboxes.csv")

#---- THERE WAS A GAME CONTROLLER
# GameOver : Timer ran out
# WinState : all letters mailed in the right mailboxes
# LoseState : != WinState 

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("mailPoster")
        self.root.geometry("600x600")
        
# GAME STATE
    ## Score
        self.score = 0 # letters posted right
        self.letters_delivered = 0 #letters posted, right or wrong
        self.wrong_deliveries = 0 #letters posted wrong
        self.missed_count = 0 #times posted wrong

    ## Time
        self.is_game_running = False
        self.day_start_time = 0
        self.day_duration = 5  # 10 seconds per day
        self.current_day = 1

# DATA
        self.all_letters = self.load_letters(letters_path)
        self.mailboxes = self.load_mailboxes(mailboxes_path)
        self.letters_today = []
        self.letters_to_deliver = [] # list of letters for today and letters wrong from previous days
        self.current_letter_index = 0 # letter to show for posting
# UI ELEMENTS
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

# METHODS

    def load_letters(self, filename):
        letters = []
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    letters.append(Letter(row['letterID'], row['recipientID'], row['day']))
        except FileNotFoundError:
            print(f"Error: Could not find {filename}")
        return letters

    def load_mailboxes(self, filename):
        mailboxes = []
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    mailboxes.append(Mailbox(row['boxID'], row['address'], row.get('color', 'white')))
        except FileNotFoundError:
            print(f"Error: Could not find {filename}")
        return mailboxes

    def start_day(self):
        if self.is_game_running:
            return # to prevent multiple start

        if not self.is_game_running:

            # clear mailboxes content from previous runs
            for mailbox in self.mailboxes:
                mailbox.containing.clear()
                mailbox.has_mail = False

            #reload letters
            self.all_letters = self.load_letters(letters_path)
            self.letter_info_var.set("New run begins...")

        # Start new day
        self.is_game_running = True
        self.day_start_time = time.time()
        self.start_button.config(state="disabled") #day started, start button off

        # Get today's letters
        self.letters_today = [l for l in self.all_letters if l.day == self.current_day and not l.ismailed]
        self.current_letter_index = 0 # show first letter of the list
        
        print(f"Starting day {self.current_day} - {len(self.letters_today)} letters found.")

        for letter in self.letters_today:
            print(f"Letter {letter.letterID} for {letter.recipientID} on day {letter.day}")
        self.letters_delivered = 0
        self.update_letter_ui()
        self.create_mailbox_buttons()
        self.update_timer()

    def update_letter_ui(self):
        total = len(self.letters_today) # toutes les lettres du jour
        if self.current_letter_index < total: # s'il reste des lettres
            letter = self.letters_today[self.current_letter_index] # show first letter
            #match id to box
            recipient_mailbox = next((mb for mb in self.mailboxes if mb.boxID == letter.recipientID), None) 
            if recipient_mailbox:
                recipient = recipient_mailbox.address # show match
            else:
                recipient = f"Unknown ({letter.recipientID})"
            total = len(self.letters_to_deliver)
            self.letter_info_var.set(f"Letter {self.current_letter_index + 1} of {total} - Deliver to {recipient}")
        else:
            self.letter_info_var.set("All letters delivered.")

    def create_mailbox_buttons(self):
        for btn in self.mailbox_buttons:
            btn.destroy()
        self.mailbox_buttons.clear()

        for mailbox in self.mailboxes:
            btn = Button(self.root, text=mailbox.address, font=("Arial", 12),
                        bg=mailbox.color, command=lambda mb=mailbox: self.post_letter(mb))
            btn.pack(pady=2)
            self.mailbox_buttons.append(btn)

    def update_timer(self):
        if self.is_game_running:
            elapsed_time = time.time() - self.day_start_time
            remaining = round(max(0, self.day_duration - elapsed_time), 1)

            if remaining > 0:
                self.timer_label.config(text=f"Time remaining: {remaining:.1f} seconds")
                self.root.after(100, self.update_timer)
            else:
                self.end_day()            

    def post_letter(self, mailbox):
        if self.current_letter_index < len(self.letters_today):
            current_letter = self.letters_today[self.current_letter_index]
            current_letter.mail(mailbox.boxID)
            mailbox.receiveMail(current_letter)

            self.letters_delivered += 1

            # Check if correct
            if current_letter.recipientID == mailbox.boxID:
                self.score += 1
            else:
                self.wrong_deliveries += 1

            self.current_letter_index += 1

            # end early if all letters are posted FINI PARTI
            if self.current_letter_index >= len(self.letters_today):
                self.end_day()

    def end_day(self):
        self.is_game_running = False
        self.timer_label.config(text="Day Over !")
        
        # Count unposted letters as wrong
        unposted_letters = self.letters_today[self.current_letter_index:]
        missed_count = len(unposted_letters)
        self.wrong_deliveries += missed_count
        self.letters_delivered += missed_count
        self.missed_count += missed_count

        # Push missed letters to next day
        for letter in unposted_letters:
            letter.day += 1
            letter.is_mailed = False

        total_today = len(self.letters_today)
        posted_today = self.letters_delivered - self.missed_count
        self.letter_info_var.set(f"Posted {posted_today} / {total_today} letters | Score: {self.score} | Wrong: {self.wrong_deliveries}")

       # Is there any letters for future days ?
        remaining_days = sorted(set(letter.day for letter in self.all_letters if letter.day > self.current_day))
        
        if remaining_days:
            self.current_day = remaining_days[0]
            self.day_label.config(text=f"Day {self.current_day}")
            self.start_button.config(state="normal", text="Start Next Day")
        else:
            never_posted = [l for l in self.all_letters if not l.is_mailed]
            missed_total = len(never_posted)

            self.letter_info_var.set(f"Game Over ! Final score: {self.score} | Wrong: {self.wrong_deliveries} | Missed forever: {missed_total}")
            self.timer_label.config(text="Game Over! All days finished.")
            self.day_label.config(text="All Days Complete")
            self.start_button.config(state="disabled")

            self.reset_button = Button(self.root, text="Reset Game", font=("Arial", 14), command=self.reset_game)
            self.reset_button.pack(pady=10)

    def reset_game(self):
        self.current_day = 1
        self.score = 0
        self.letters_delivered = 0
        self.wrong_deliveries = 0
        self.missed_count = 0        
        self.is_game_running = False

        self.all_letters = self.load_letters(letters_path)

        # Clean up UI
        self.timer_label.config(text="Press Start to begin")
        self.day_label.config(text=f"Day {self.current_day}")
        self.letter_info_var.set("Click Start to begin.")
        self.start_button.config(state="normal", text="Start Day")

        # Remove reset button if it exists
        if hasattr(self, 'reset_button'):
            self.reset_button.destroy()

##---------- THE GAME TRACKS THE SCORE
# It allocates time to play based on number of letters to deliver
# It check if player posted right

##----------- THE GAME CHECKS IF PLAYER POSTED RIGHT

# IT CAN LOOKUP addressES
"""
    def find(element, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == element:
                    return (i,j)

    def findBox_name(box_id, matrix):
        box_id_pos = find(box_id, matrix)[0]
        return matrix[box_id_pos,1]

    def findBox_address(box_id, matrix):
        box_id_pos = find(box_id, matrix)[0]
        return matrix[box_id_pos,2]

    def findBox_color(box_id, matrix):
        box_id_pos = find(box_id, matrix)[0]
        return matrix[box_id_pos,3]

    def findBox_id(element, matrix):
        box_id_pos = find(element, matrix)[0]
        return matrix[box_id_pos,0]
"""
# print('name : '+findBox_name('M2', pdMatrix))
# print('address : '+findBox_address('M2', pdMatrix))
# print('box color : '+findBox_color('M2', pdMatrix))
# print('box id : '+findBox_id('Mr.Red', pdMatrix))# THE GAME CAN LOOKUP addressES
"""
def find(element, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == element:
                return (i,j)

def findBox_name(box_id, matrix):
    box_id_pos = find(box_id, matrix)[0]
    return matrix[box_id_pos,1]

def findBox_address(box_id, matrix):
    box_id_pos = find(box_id, matrix)[0]
    return matrix[box_id_pos,2]

def findBox_color(box_id, matrix):
    box_id_pos = find(box_id, matrix)[0]
    return matrix[box_id_pos,3]

def findBox_id(element, matrix):
    box_id_pos = find(element, matrix)[0]
    return matrix[box_id_pos,0]
"""
# print('name : '+findBox_name('M2', pdMatrix))
# print('address : '+findBox_address('M2', pdMatrix))
# print('box color : '+findBox_color('M2', pdMatrix))
# print('box id : '+findBox_id('Mr.Red', pdMatrix))




## WE MAIL LETTERS TO BOXES
"""
def ClickButton(postedLetters, score):
    postedLetters += 1
    ShowScore["text"] = "You posted " + str(postedLetters) + " letters."


#UI
ShowScore = Label(root, text="No letter posted", font=("Arial, 10"),fg="purple")

LetteraddressText=StringVar(value="The next letter is for " + letters[0].recipientID)

ShowFirstLetter = Label(root, textvariable=LetteraddressText, font=("Arial, 10"),fg="purple")"""

"""
for mailbox in mailboxes:  
    mailboxText=StringVar(value=mailbox.address)
    mailBoxUI = Button(root, textvariable=mailboxText, font=("Arial, 15"), command=ClickButton)
    mailBoxUI.pack()

ShowScore.pack()
ShowFirstLetter.pack()"""

if __name__ == '__main__':
    root = Tk()
    game = Game(root)
    root.mainloop()


"""TO DO
- Implement posting mechanic to put letters in mailboxes on ClickButton Function
- Implement scoreManager to check if letters are rightly posted
    I want to compare letter.recipientID et letter.postedID to know if a letter is rightly posted
    I want to read mailbox.containing to access letters in said mailbox.
    I want to match ID to string of letters. For example, M1 = "Mr. Green", L1 = "for" + M1. Il me faut une matrice. Et ensuite je peux l'auto remplir avec le CSV peut-être ? https://www.geeksforgeeks.org/python-matrix/
- Implement game over (mis en place une classe game pour éviter les variables globales. Ça casse l'UI et certaines fonctions pour l'instant. À corriger.)
- Implement csv reader to autocreate letters and mailboxes according to table. https://www.geeksforgeeks.org/how-to-create-a-list-of-object-in-python-class/ https://stackoverflow.com/questions/49614798/how-to-extract-specific-data-from-a-csv-file-with-given-parameters
- CSV implemented. Ça marche avec les mailboxes et les méthodes de Vlookup. Reste à mettre les lettres en face et à coder la vérif.
- Implemented Timer from Claude. To DO : fix the timer script to use the simplified Claude writing. Le code suppose un bouton pour lancer la journée et un temps fixe de journée. Il manque la prépa, le calendrier et le calcul du score. 
- j'aimerais randomiser les lettres à partir d'un CSV et créer les assets visuels associés qu'on verrait dans l'affichage de la lettre actuelle.
"""
