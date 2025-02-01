import logging
import time
import datetime

# Variables de base
seconds = time.time()
localTime = time.ctime(seconds)
currentTime = datetime.datetime.now()
currentTimeNextYear = datetime.datetime(currentTime.year + 1, 1, 1)
currentTimeNextYearAlt = currentTime + datetime.timedelta(days=365)

timerTime = 0
timerDeadline = 0

# blocks

## TO know time I ask the clock what time it is
def clockTime():
    return time.time()

## TO set the countdown I ask the timer value

def setTimer():
    global timerTime
    timerTime = int(input("Enter the countdown time in seconds : "))
    return timerTime

## TO set the deadline I add the timer to the actual time

def setDeadline():
    global timerTime
    return timerTime + clockTime()

## TO run the countdown I ask for a go

def runCountdown():
    input("Press Enter to start the countdown")
    return True

## TO pause the countdown I ask for a pause

def pauseCountdown():
    input("Press Enter to pause the countdown")
    return True

## TO stop the countdown I ask for an input

def stopCountdown():  
    input("Press Enter to stop the countdown")
    return True 

## TO obtain the remaining time I substrack the time to the deadline

def remainingTime():
    global timerTime
    return timerTime - clockTime()


## TO display the countdown I print the remaining time


def displayCountdown():
    global timerTime
    print("Time remaining : ", timerTime)

## TO check if countdown over I compare the deadline and the actual time

def countdownOver():
    global timerTime
    return timerTime < clockTime()

## TO signal countdown over I print the alarm


## TO know if start over I ask for input

## TO start over I clean the variables and launch again

# main init
setTimer()
runCountdown()
