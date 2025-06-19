from tkinter import *
import csv
import time

"""STORY
You have 2 mailboxes and a stack of letters.
You post the letters one by one to the mailboxes and try to match the adresses. This is your score.
Once you have no mail left, game over.
"""

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

"""
letter1 = letter("L1", "M1")
letter2 = letter("L2", "M2")
letters = [letter1, letter2]

def checkLetters():
    print("DEBUG_Letters")
    for letter in letters:
        print("Adress: For {adress}; mailed: {status}".format(adress=letter.recipientID, status = letter.is_mailed))

checkLetters()
"""
##--- MAILBOXES

class Mailbox():
    def __init__(self, boxID, adress, color="white"):
        self.boxID = boxID
        self.address = adress
        self.has_mail = False
        self.color = "white"
        self.containing = []
    
    def receiveMail(self, letter):
        self.containing.append(letter)
        self.has_mail = True

"""mailbox1 = mailbox("M1","Mr.Red")
mailbox2 = mailbox("M2","Mr.Green")
mailboxes = [mailbox1, mailbox2]

def checkMailboxes():
    print("DEBUG_Mailboxes")
    for mailbox in mailboxes:
        print("On the box is written a name: {name}".format(name = mailbox.adress) + "Box contains mail: {status}".format(status=mailbox.has_mail))

checkMailboxes()"""

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
        self.score = 0
        self.letters_delivered = 0
        self.wrong_deliveries = 0
        
    ## Time
        self.is_game_running = False
        self.day_start_time = 0
        self.day_duration = 5  # 10 seconds per day
        self.current_day = 1

# DATA
        self.all_letters = self.load_letters()
        """("letters.csv")"""
        self.mailboxes = self.load_mailboxes()
        """("mailboxes.csv")"""
        self.letters_today = []

# UI ELEMENTS
        self.timer_label = Label(root, text="Press Start to begin", font=("Arial", 16))
        self.timer_label.pack(pady=20)

        self.score_label = Label(root, text="Score: 0", font=("Arial", 12),fg="green")
        self.score_label.pack()

        self.letter_info_var = StringVar(value="No letters yet.")
        self.letter_label = Label(root, textvariable=self.letter_info_var,font=("Arial", 14), fg="purple")
        self.letter_label.pack(pady=10)

        self.start_button = Button(root, text="Start Day", command=self.start_day, font=("Arial", 14))
        self.start_button.pack(pady=10)

        self.mailbox_buttons = []

# METHODS

    def load_letters(self):
        letter1 = Letter("L1", "M1", 1)
        letter2 = Letter("L2", "M2", 2)
        letter3 = Letter("L3", "M1", 2)
        letter4 = Letter("L4", "M2", 2)
        letters = [letter1, letter2, letter3, letter4]
        return letters
        """
        letters = []
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    letters.append(Letter(row['LetterID'], row['RecipientID'], row['Day']))
        except FileNotFoundError:
            print(f"Error: Could not find {filename}")
        return letters
        """

    def load_mailboxes(self):
        mailbox1 = Mailbox("M1","Mr.Red","red")
        mailbox2 = Mailbox("M2","Mr.Green","green")
        mailboxes = [mailbox1, mailbox2]
        return mailboxes
        """
        mailboxes = []
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    mailboxes.append(Mailbox(row['BoxID'], row['Address'], row.get('Color', 'white')))
        except FileNotFoundError:
            print(f"Error: Could not find {filename}")
        return mailboxes
        """
    def start_day(self):
        if not self.is_game_running:
            self.is_game_running = True
            self.day_start_time = time.time()
            self.letters_today = [l for l in self.all_letters if l.day == self.current_day]
            self.current_letter_index = 0
            self.update_letter_ui()
            self.create_mailbox_buttons()
            self.update_timer()

    def update_letter_ui(self):
        if self.current_letter_index < len(self.letters_today):
            current_letter = self.letters_today[self.current_letter_index]
            current_letter.mail(Mailbox.boxID)
            Mailbox.receiveMail(current_letter)

            # Check correctness
            if current_letter.recipientID == Mailbox.boxID:
                self.score += 1
            else:
                self.wrong_deliveries += 1

            self.letters_delivered += 1
            self.current_letter_index += 1

            self.score_label.config(text=f"Score: {self.score}")
            self.update_letter_ui()

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

    def end_day(self):
        self.is_game_running = False
        self.timer_label.config(text="Game Over !")
        self.letter_info_var.set(f"Posted {self.letters_delivered} letters | Score: {self.score}")

    def post_letter(self, mailbox):
        if self.current_letter_index < len(self.letters_today):
            current_letter = self.letters_today[self.current_letter_index]
            current_letter.mail(mailbox.boxID)
            mailbox.receiveMail(current_letter)

            # Check if correct
            if current_letter.recipientID == mailbox.boxID:
                self.score += 1
            else:
                self.wrong_deliveries += 1

            self.current_letter_index += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.update_letter_ui()

##---------- THE GAME TRACKS THE SCORE
# It allocates time to play based on number of letters to deliver
# It check if player posted right

##----------- THE GAME CHECKS IF PLAYER POSTED RIGHT

# IT CAN LOOKUP ADRESSES
"""
    def find(element, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == element:
                    return (i,j)

    def findBox_name(box_id, matrix):
        box_id_pos = find(box_id, matrix)[0]
        return matrix[box_id_pos,1]

    def findBox_adress(box_id, matrix):
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
# print('adress : '+findBox_adress('M2', pdMatrix))
# print('box color : '+findBox_color('M2', pdMatrix))
# print('box id : '+findBox_id('Mr.Red', pdMatrix))# THE GAME CAN LOOKUP ADRESSES
"""
def find(element, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == element:
                return (i,j)

def findBox_name(box_id, matrix):
    box_id_pos = find(box_id, matrix)[0]
    return matrix[box_id_pos,1]

def findBox_adress(box_id, matrix):
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
# print('adress : '+findBox_adress('M2', pdMatrix))
# print('box color : '+findBox_color('M2', pdMatrix))
# print('box id : '+findBox_id('Mr.Red', pdMatrix))




## WE MAIL LETTERS TO BOXES
"""
def ClickButton(postedLetters, score):
    postedLetters += 1
    ShowScore["text"] = "You posted " + str(postedLetters) + " letters."


#UI
ShowScore = Label(root, text="No letter posted", font=("Arial, 10"),fg="purple")

LetterAdressText=StringVar(value="The next letter is for " + letters[0].recipientID)

ShowFirstLetter = Label(root, textvariable=LetterAdressText, font=("Arial, 10"),fg="purple")"""

"""
for mailbox in mailboxes:  
    mailboxText=StringVar(value=mailbox.Adress)
    mailBoxUI = Button(root, textvariable=mailboxText, font=("Arial, 15"), command=ClickButton)
    mailBoxUI.pack()

ShowScore.pack()
ShowFirstLetter.pack()"""


if __name__ == '__main__':
    root = Tk()
    game = Game(root)
    root.mainloop()