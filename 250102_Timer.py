import logging
import time
import datetime

# Variables de base
global timerDuration
global timerDeadline

#methods

def clockTime():
    return time.time()

def setTimerDuration():
    global timerDuration
    timerDuration = int(input("Enter the duration of the timer in seconds : "))
    return timerDuration

def isTimerSet():
    return timerDuration > 0

def setDeadline():
    global timerDeadline
    timerDeadline = timerDuration + clockTime()
    return timerDeadline

def timeRemaining():
    t = timerDeadline - clockTime()
    return round(t,1)

def resetTimer():
    global timerDuration
    global timerDeadline
    timerDuration = 0
    timerDeadline = 0

def launchTimer():
    input("Press Enter to start the timer.")
    setDeadline()
    return True
    
# main init
setTimerDuration()
print()
while isTimerSet():
    launchTimer()
    print()
    while clockTime() < timerDeadline:
        print("Time remaining : ", timeRemaining(), end='\r')
        time.sleep(1)
    print()
    print("Time's up !")
    resetTimer()
    print()
    setTimerDuration()

'''
end='\r' is a carriage return, 
it moves the cursor to the beginning of the line, 
so that the next print will overwrite the previous one.
'''