#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from PIL import ImageTk,Image

app = Tk()
app.title("Welcome")
image2 =Image.open(r'.\IMGS\a03.png')
background_image = ImageTk.PhotoImage(image2)
w = background_image.width()
h = background_image.height()
app.geometry('%dx%d+0+0' % (w,h))

background_label = Label(app, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

for x in ('button1','button2','button3'):
    btn=Button(app,text=x)
    btn.pack()
    
app.mainloop()
