import tkinter as tk

from PIL import Image, ImageTk
im = Image.open("foregroundPostman.png")
print(im.mode)

root = tk.Tk()
root.title("Frame Demo")
root.config(bg="skyblue")
canvas = tk.Canvas(root, width=1600, height = 900)
canvas.pack()

image = Image.open("foregroundPostman.png").convert("RGBA")

print(image.mode, image.size)

tk_image = ImageTk.PhotoImage(image)

canvas.image = tk_image

frame = tk.Frame(canvas, width=600, height=600,bg="red")
label = tk.Label(frame, text="This is a frame", bg="red")
label.pack()
canvas.create_window(100, 100, window=frame, anchor='nw')

id1 = canvas.create_image(0,900, image=canvas.image, anchor='sw')

canvas.tag_raise(id1)

#pack(padx=5, pady=5,side=tk.RIGHT, fill=tk.Y)

root.mainloop()