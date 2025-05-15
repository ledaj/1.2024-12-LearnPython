from tkinter import *
root = Tk()
root.geometry("300x300")
root.title("MOO ICT Button Clicker")
number = 0
# add the button function here
def ClickButton():
    global number
    number += 1
    ShowInfo["text"] = "You Clicked " + str(number) + " times."
ClickingButton = Button(root,text="Click Me!", padx=50, pady=50, bg="gold", font=("Arial, 22"), command=ClickButton)
ShowInfo = Label(root, text="message", font=("Arial, 20"), fg="purple", pady=20)
ClickingButton.pack()
ShowInfo.pack()
root.mainloop()