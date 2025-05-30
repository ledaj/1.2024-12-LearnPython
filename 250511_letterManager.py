#create letters
class letter():
    def __init__(self, recipientAdress):
        self.recipientAdress = recipientAdress
        self.isMailed = False

    def checkRecipientAdress(self):
        if self.recipientAdress != "":
         print(f"The letter is adressed to {self.recipientAdress}.")
        else:
            print(f"The letter has no recipient adress written on it.")
    def mail(self):
        self.isMailed = True

    def checkMailStatus(self):
        print(self.isMailed)

letter1 = letter("For Mr.Red")
letter2 = letter("For Mr.Green")

#create bagOfLetters

bagOfLetters = [letter2, letter1]

def checkBagOfLetters():
    for letter in bagOfLetters:
        print("Adress: {adress}; status: {status}".format(adress=letter.recipientAdress, status = letter.isMailed))

def removeLetterFromBag(letter):
    bagOfLetters.remove(letter)

checkBagOfLetters