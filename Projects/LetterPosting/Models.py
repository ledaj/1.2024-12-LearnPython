import csv
import os
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

def load_letters(filename):
    letters = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                letters.append(Letter(row['letterID'], row['recipientID'], row['day']))
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
    return letters

def load_mailboxes(filename):
    mailboxes = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                mailboxes.append(Mailbox(row['boxID'], row['address'], row['screen'], row.get('color', 'white')))
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
    return mailboxes