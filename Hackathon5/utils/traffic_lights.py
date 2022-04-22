# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 23:34:12 2022

@author: KESHAV
"""

import time
from time import sleep
from tkinter import *
tk=Tk()
win=Canvas(tk, width=55, height=200)
win.pack()
#functions
def red(a):
    for i in range(a):
        red=win.create_oval(5,5,50,50, fill="red")
        tk.update()
        time.sleep(0.05)
def redb(a):
    for i in range(a):
        red=win.create_oval(5,5,50,50, fill="black")
        tk.update()
        time.sleep(0.05)
def amber(a):
    for i in range(a):
        amber=win.create_oval(5,55,50,100, fill="orange")
        tk.update()
        time.sleep(0.05)
def amberb(a):
    for i in range(a):
        amber=win.create_oval(5,55,50,100, fill="black")
        tk.update()
        time.sleep(0.05)
def green(a):
    for i in range(a):
        green=win.create_oval(5,105,50,150, fill="green")
        tk.update()
        time.sleep(0.05)
def greenb(a):
    for i in range(a):
        green=win.create_oval(5,105,50,150, fill="black")
        tk.update()
        time.sleep(0.05)
def lights():
    red=win.create_oval(5,5,50,50, fill="black")
    amber=win.create_oval(5,55,50,100, fill ="black")
    green=win.create_oval(5,105,50,150, fill="black")
    #end of functions
    #calling the functions
    
lights()
red(30)
redb(1)
amber(10)
amberb(1)
green(30)
greenb(1)

tk.mainloop()