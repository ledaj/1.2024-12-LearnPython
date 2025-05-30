from tkinter import *
root = Tk()
root.geometry("600x600")
root.title("mailPoster")

"""STORY
You have 2 mailboxes and a stack of letters.
You post the letters one by one to the mailboxes and try to match the adresses. This is your score.
Once you have no mail left, game over.
"""

#create letters
class letter():
    def __init__(self, recipientAdress, mailboxID):
        self.recipientAdress = recipientAdress
        self.mailboxID = mailboxID
        self.isMailed = False

    def mail(self):
        self.isMailed = True

letter1 = letter("Mr.Red", 1)
letter2 = letter("Mr.Green", 2)
Letters = [letter1, letter2]

def checkBagOfLetters():
    print("DEBUG_Letters")
    for letter in Letters:
        print("Adress: For {adress}; mailed: {status}".format(adress=letter.recipientAdress, status = letter.isMailed))

checkBagOfLetters()

#create Mailboxes
class mailbox():
    def __init__(self, recipientName, mailboxID):
        self.recipientName = recipientName
        self.hasMail = False
        self.mailboxID = mailboxID
    
    def receiveMail(self):
        self.hasMail = True

mailbox1 = mailbox("Mr.Red", 1)
mailbox2 = mailbox("Mr.Green", 2)
mailboxes = [mailbox1, mailbox2]

def checkMailboxes():
    print("DEBUG_Mailboxes")
    for mailbox in mailboxes:
        print("On the box is written a name: {name}".format(name = mailbox.recipientName) + "Box contains mail: {status}".format(status=mailbox.hasMail))

checkMailboxes()

#UI
postedLetters = 0
score = 0

def ClickButton(postedLetters, score):
    postedLetters += 1
    ShowInfo["text"] = "You posted " + str(postedLetters) + " letters."

ShowInfo = Label(root, text="No letter posted",font=("Arial, 10"),fg="purple")
ShowInfo.pack()

for mailbox in mailboxes:  
    mailboxText=StringVar(value="{name}".format(name = mailbox.recipientName))
    mailBoxUI = Button(root, textvariable=mailboxText, font=("Arial, 15"), command=ClickButton)
    mailBoxUI.pack()

root.mainloop()


