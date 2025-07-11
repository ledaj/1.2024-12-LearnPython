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
    def __init__(self, boxID, address, screen, color="white"):
        self.boxID = boxID
        self.address = address
        self.has_mail = False
        self.color = color
        self.screen = int(screen)
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
        self.root.geometry("800x600")
        
    # GAME STATE
        ## Score
        self.score = 0 # letters posted right
        self.letters_delivered = 0 #letters posted, right or wrong
        self.wrong_deliveries = 0 #letters posted wrong
        self.missed_count = 0 #times posted wrong

        ## Time
        self.is_game_running = False
        self.day_start_time = 0
        self.day_duration = 10  # 10 seconds per day
        self.current_day = 1

        ## Screen
        self.current_screen = 0

    # DATA
        self.all_letters = self.load_letters(letters_path)
        self.mailboxes = self.load_mailboxes(mailboxes_path)
        self.letters_today = [] # loaded letters for the day
        self.letters_to_deliver = [] # list of letters for today and letters wrong from previous days
        self.current_letter_index = 0 # first letter to show for posting UI
        
    # UI ELEMENTS
        self.timer_label = Label(root, text="Press Start to begin", font=("Arial", 16))
        self.timer_label.pack(pady=20)
        # self.timer_canvas = Canvas(self.root, width=300, height=20, bg="white")
        # self.timer_canvas.pack(pady=5)
        # self.timer_gauge = self.timer_canvas.create_rectangle(0,0,300,20, fill="green")

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

    # KEY BINDINGS
        self.last_selected_button = None
        self.key_mapped_buttons = {}

        self.root.bind("<a>", self.prev_screen)
        self.root.bind("<e>", self.next_screen)
        self.update_screen_label()
        self.root.bind("<q>", self.key_post_left)
        self.root.bind("<d>", self.key_post_right)
        self.root.bind("<space>", self.key_post_current)

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
                    mailboxes.append(Mailbox(row['boxID'], row['address'], row['screen'], row.get('color', 'white')))
        except FileNotFoundError:
            print(f"Error: Could not find {filename}")
        return mailboxes

    def prev_screen(self, event=None):
        self.current_screen = max(0, self.current_screen - 1)
        self.create_mailbox_buttons()
        self.update_screen_label()

    def next_screen(self, event=None):
        self.current_screen += 1
        # check if any mailboxes exist on the new screen
        if any(mb.screen == self.current_screen for mb in self.mailboxes):
            self.create_mailbox_buttons()
            self.update_screen_label()
        else:
            self.current_screen -= 1 #revert if no more screens

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
        self.letters_today = [l for l in self.all_letters if l.day == self.current_day]
        self.current_letter_index = 0 # show first letter of the list
        
        print(f"Starting day {self.current_day} - {len(self.letters_today)} letters found.")

        for letter in self.letters_today:
            print(f"Letter {letter.letterID} for {letter.recipientID} on day {letter.day}")
        self.letters_delivered = 0
        self.update_letter_ui()
        self.current_screen = 0
        self.create_mailbox_buttons()
        self.update_timer()
        self.update_screen_label()

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
            self.letter_info_var.set(f"Letter {self.current_letter_index + 1} of {total} - Deliver to {recipient}")
        else:
            self.letter_info_var.set("All letters delivered.")

    def create_mailbox_buttons(self):
        # destroy previous buttons
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

    def update_timer(self):
        if self.is_game_running:
            elapsed_time = time.time() - self.day_start_time
            remaining = round(max(0, self.day_duration - elapsed_time), 1)
            percent_left = remaining / self.day_duration
          
            #width = 300 * percent_left
            #color = "green" if percent_left > 0.3 else "red"
            #self.timer_canvas.coords(self.timer_gauge, 0,0,width,20)
            #self.timer_canvas.itemconfig(self.timer_gauge, fill=color)

            if remaining > 0:
                self.timer_label.config(text=f"Time remaining: {remaining:.1f} seconds")
                self.root.after(100, self.update_timer)
            else:
                self.end_day()            

    def update_screen_label(self):
        self.screen_label.config(text=f"Screen {self.current_screen} — Press A/E to switch screens")

    def post_letter(self, mailbox, button_index=None):

        if self.current_letter_index < len(self.letters_today): # if you still ot letters to post
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
            self.update_letter_ui()
            self.last_selected_mailbox = mailbox

            #Highlight pressed button
            """
            if button_index is not None:
                if self.last_selected_buttonselected_button is not None:
                    self.last_selected_button.config(relief=RAISED)
                self.last_selected_button = self.mailbox_buttons[button_index]
                self.last_selected_button.config(relief=SUNKEN)
            """


            # end early if all letters are posted FINI PARTI
            if self.current_letter_index >= len(self.letters_today):
                self.end_day()
    
    def key_post_left(self, event):
        if 'q' in self.key_mapped_buttons:
            self.post_letter(self.key_mapped_buttons['q'], 0)

    def key_post_right(self, event):
        if 'd' in self.key_mapped_buttons:
            self.post_letter(self.key_mapped_buttons['d'], 0)

    def key_post_current(self, event):
        if hasattr(self, 'last_selected_mailbox'):
            self.post_letter(self.last_selected_mailbox)

    def end_day(self):
        self.is_game_running = False
        self.timer_label.config(text="Day Over !")
    
        total_today = len(self.letters_today)
        posted_today = self.letters_delivered
        self.letter_info_var.set(f"Posted {posted_today} / {total_today} letters | Score: {self.score} | Wrong: {self.wrong_deliveries}")

       # Is there any letters for future days ?
        remaining_days = sorted(set(letter.day for letter in self.all_letters if letter.day > self.current_day))
        
        if remaining_days:
            self.current_day = remaining_days[0]
            self.day_label.config(text=f"Day {self.current_day}")
            self.start_button.config(state="normal", text="Start Next Day")
        else:

            self.letter_info_var.set(f"Game Over ! Final score: {self.score} | Wrong: {self.wrong_deliveries}")
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
- jauge de temps qui descend et qui devient rouge plus ça descend
- mapper des touches pour les boites aux lettres, ou tout mapper au clavier : q d et espace pour poster
"""
