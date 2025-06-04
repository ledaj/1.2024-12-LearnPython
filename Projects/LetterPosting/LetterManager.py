from tkinter import *
import csv
root = Tk()
root.geometry("600x600")
root.title("mailPoster")

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
- Implement game over
- Implement csv reader to autocreate letters and mailboxes according to table. https://www.geeksforgeeks.org/how-to-create-a-list-of-object-in-python-class/ https://stackoverflow.com/questions/49614798/how-to-extract-specific-data-from-a-csv-file-with-given-parameters
"""
#ELEMENTS OF PLAY

## THERE WERE LETTERS
class letter():
    def __init__(self, letterID, recipientID):
        self.letterID = letterID
        #self.senderID = senderID
        self.recipientID = recipientID
        self.postedID = postedID = ""
        self.isMailed = False

    def mail(self, postedID):
        self.postedID = postedID
        self.isMailed = True

letter1 = letter("L1", "M1")
letter2 = letter("L2", "M2")
letters = [letter1, letter2]

def checkLetters():
    print("DEBUG_Letters")
    for letter in letters:
        print("Adress: For {adress}; mailed: {status}".format(adress=letter.recipientID, status = letter.isMailed))

checkLetters()

## THERE WERE MAILBOXES
class mailbox():
    def __init__(self, boxID, Adress):
        self.boxID = boxID
        self.Adress = Adress
        self.hasMail = False
        self.color = "white"
        self.containing = []
    
    def receiveMail(self, letterID):
        self.containing.append("{ID}".format(ID=letterID))
        self.hasMail = True

mailbox1 = mailbox("M1","Mr.Red")
mailbox2 = mailbox("M2","Mr.Green")
mailboxes = [mailbox1, mailbox2]

def checkMailboxes():
    print("DEBUG_Mailboxes")
    for mailbox in mailboxes:
        print("On the box is written a name: {name}".format(name = mailbox.Adress) + "Box contains mail: {status}".format(status=mailbox.hasMail))

checkMailboxes()

## WE MAIL LETTERS TO BOXES





def ClickButton(postedLetters, score):
    postedLetters += 1
    ShowScore["text"] = "You posted " + str(postedLetters) + " letters."



# WE COUNT THE SCORE
postedLetters = 0
score = 0

#UI
ShowScore = Label(root, text="No letter posted", font=("Arial, 10"),fg="purple")

LetterAdressText=StringVar(value="The next letter is for " + letters[0].recipientID)

ShowFirstLetter = Label(root, textvariable=LetterAdressText, font=("Arial, 10"),fg="purple")


for mailbox in mailboxes:  
    mailboxText=StringVar(value=mailbox.Adress)
    mailBoxUI = Button(root, textvariable=mailboxText, font=("Arial, 15"), command=ClickButton)
    mailBoxUI.pack()

ShowScore.pack()
ShowFirstLetter.pack()
root.mainloop()


