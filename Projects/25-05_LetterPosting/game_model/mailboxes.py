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