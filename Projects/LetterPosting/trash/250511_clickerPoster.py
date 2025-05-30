from tkinter import *
root = Tk()
root.geometry("600x600")
root.title("mailPoster")
postedLetters = 0

def ClickButton():
    global postedLetters
    postedLetters += 1
    ShowInfo["text"] = "You posted " + str(postedLetters) + " letters."
Letterbox1 = Button(root, text="M. Rouge", bg="red", font=("Arial, 22"), command=ClickButton)
Letterbox2 = Button(root, text="M. Green", bg="green", font=("Arial, 22"), command=ClickButton)
ShowInfo = Label(root, text="No letter posted",font=("Arial, 20"),fg="purple")
Letterbox1.pack()
Letterbox2.pack()
ShowInfo.pack()
root.mainloop()
