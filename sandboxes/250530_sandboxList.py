LetterStack = ["Red", "Green"]

print(LetterStack)
print(len(LetterStack))
print(LetterStack[1])

print(LetterStack)
print(len(LetterStack))

def showActiveLetter():
    print("The first letter on stack is {letter}".format(letter=LetterStack[0]))

def postActiveLetter():
    LetterStack.pop(0)
    #increment postedLetters
    #check if correct posting

showActiveLetter()
postActiveLetter()
showActiveLetter()