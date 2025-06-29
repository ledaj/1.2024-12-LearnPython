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