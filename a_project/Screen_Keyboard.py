#from functools import partial
from tkinter import *
import tkinter
import os
import threading
import time
from threading import Thread
from pynput.mouse import Button, Controller



global Keyboard_App
Keyboard_App = tkinter.Tk()
Keyboard_App.title("virtual Keyboard")
Keyboard_App ['bg']='white'
Keyboard_App.resizable(0,0)
path = '@%s' % os.path.join(os.environ['WINDIR'], 'Cursors/arrow_r.cur').replace('\\', '/')
Keyboard_App.config(cursor=path)
Keyboard_App.geometry("520x540+1+1")

            
def select(value):
    if value == "RESET":
        entry.delete(0,END)
    elif value == " Space ":
        entry.insert(END, ' ')
    elif value == "<-" :
        entry.delete(len(entry.get())-1,END)

    else:
        entry.insert(END, value)
 
buttons = [
    'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z', '?',' Space ', 'RESET',
    '<-']
labell = Label (Keyboard_App, text="eye messenger", font =('arial', 30, 'bold'),
                    
    bg ='white', fg="#000000").grid(row = 0, columnspan = 16)

entry = Entry(Keyboard_App, width=40,   font =('arial', 14, 'bold'))

entry.grid(row = 1, columnspan = 40)

varRow = 3
varColumn = 0

for button in buttons:
    command = lambda x=button: select(x)
    tkinter.Button(Keyboard_App, text = button, width =5, bg="pink", fg="#000000",
                    activebackground="#ffffff", activeforeground="#000990", relief = 'raised'
                       ,padx=20, pady=20, bd=5, font = ('arial', 12, 'bold'),
                       command = command).grid(row = varRow, column = varColumn)


    varColumn+=1
    if varColumn > 4 and varRow == 3:
        varColumn   = 0
        varRow+=1
    if varColumn   >4 and varRow ==4:
        varColumn   = 0
        varRow+=1
    if varColumn   >4 and varRow ==5:
        varColumn   = 0
        varRow+=1
    if varColumn   >4 and varRow ==6:
        varColumn   = 0
        varRow+=1
    if varColumn   >4 and varRow ==7:
        varColumn   = 0
        varRow+=1


mouse = Controller()

mouse.position = (80, 140)
Keyboard_App.update()
time.sleep(2)

mouse.position = (180, 140)
Keyboard_App.update()
time.sleep(2)
 
mouse.position = (290, 140)
Keyboard_App.update()
time.sleep(2)

    
    
   
Keyboard_App.mainloop()


 
  
   
