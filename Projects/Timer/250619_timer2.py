import time
import tkinter as tk

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Timer")
        self.isGameRunning = False
        self.dayStartTime = 0
        self.dayDuration = 10  # in seconds

        # GUI Elements
        self.label = tk.Label(root, text="Press Start to begin", font=("Arial", 16))
        self.label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start Timer", command=self.startDay, font=("Arial", 14))
        self.start_button.pack(pady=10)

    def startDay(self):
        if not self.isGameRunning:
            self.isGameRunning = True
            self.dayStartTime = time.time()
            self.updateTimer()

    def updateTimer(self):
        if self.isGameRunning:
            elapsedTime = time.time() - self.dayStartTime
            remaining = round(max(0, self.dayDuration - elapsedTime), 1)

            if remaining > 0:
                self.label.config(text=f"Time remaining: {remaining:.1f} seconds")
                self.root.after(100, self.updateTimer)  # smoother update (100ms)
            else:
                self.endDay()

    def endDay(self):
        self.isGameRunning = False
        self.label.config(text="Game Over!")

# Tkinter setup
root = tk.Tk()
game = Game(root)
root.mainloop()
