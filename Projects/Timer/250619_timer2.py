import time

# No need for tkinter here since you're using input() and print()
class Game:
    def __init__(self):
        self.isGameRunning = False
        self.dayStartTime = 0
        self.dayDuration = 10  # 10 seconds per day for testing

    def launchTimer(self):
        input("Press Enter to start the timer.")
        self.startDay()

    def startDay(self):
        self.isGameRunning = True
        self.dayStartTime = time.time()
        print("DEBUG : isGameRunning :", self.isGameRunning)
        self.updateTimer()

    def updateTimer(self):
        while self.isGameRunning:
            elapsedTime = time.time() - self.dayStartTime
            remaining = max(0, self.dayDuration - elapsedTime)

            print(f"Time remaining: {remaining:.1f} seconds", end='\r')

            if remaining <= 0:
                self.endDay()
                break

            time.sleep(1)

    def endDay(self):
        print("\nDEBUG : endDay")
        self.isGameRunning = False
        print("DEBUG : isGameRunning :", self.isGameRunning)
        print("GameOver")

theGame = Game()

theGame.launchTimer()

