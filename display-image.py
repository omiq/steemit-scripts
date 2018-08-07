import time
from tkinter import *
from PIL import ImageTk, Image
root = Tk()
canvas = Canvas(root, width=1280, height=720)
canvas.pack()

while True:
    img = ImageTk.PhotoImage(Image.open("input.jpg"))
    canvas.create_image(0, 0, anchor=NW, image=img)
    time.sleep(0.10)
    root.mainloop()