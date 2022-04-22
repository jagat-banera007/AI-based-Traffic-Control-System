# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 23:34:12 2022

@author: KESHAV
"""

import time
from time import sleep
from tkinter import *
tk=Tk()
win=Canvas(tk, width=400, height=450)
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
    

#functions
def red1(a):
    for i in range(a):
        red=win.create_oval(10, 10, 110, 110, fill="red")
        tk.update()
        time.sleep(0.05)
def redb1(a):
    for i in range(a):
        red=win.create_oval(10, 10, 110, 110, fill="black")
        tk.update()
        time.sleep(0.05)
def amber1(a):
    for i in range(a):
        amber=win.create_oval(120, 10, 220, 110, fill="orange")
        tk.update()
        time.sleep(0.05)
def amberb1(a):
    for i in range(a):
        amber=win.create_oval(120, 10, 220, 110, fill="black")
        tk.update()
        time.sleep(0.05)
def green1(a):
    for i in range(a):
        green=win.create_oval(230, 10, 330, 110, fill="green")
        tk.update()
        time.sleep(0.05)
def greenb1(a):
    for i in range(a):
        green=win.create_oval(230, 10, 330, 110, fill="black")
        tk.update()
        time.sleep(0.05)
def lights1():
    red=win.create_oval(10, 10, 110, 110, fill="black")
    amber=win.create_oval(120, 10, 220, 110, fill ="black")
    green=win.create_oval(30,30,50,150, fill="black")
    #end of functions
    #calling the functions    

#functions
def red2(a):
    for i in range(a):
        red=win.create_oval(110,280,170,340, fill="red")
        tk.update()
        time.sleep(0.05)
def redb2(a):
    for i in range(a):
        red=win.create_oval(110,280,170,340, fill="black")
        tk.update()
        time.sleep(0.05)
def amber2(a):
    for i in range(a):
        amber=win.create_oval(110,190,170,250, fill="orange")
        tk.update()
        time.sleep(0.05)
def amberb2(a):
    for i in range(a):
        amber=win.create_oval(110,190,170,250, fill="black")
        tk.update()
        time.sleep(0.05)
def green2(a):
    for i in range(a):
        green=win.create_oval(110,100,170,160, fill="green")
        tk.update()
        time.sleep(0.05)
def greenb2(a):
    for i in range(a):
        green=win.create_oval(110,100,170,160, fill="black")
        tk.update()
        time.sleep(0.05)
def lights2():
    red=win.create_oval(110,280,170,340, fill="black")
    amber=win.create_oval(110,190,170,250, fill ="black")
    green=win.create_oval(110,100,170,160, fill="black")
    #end of functions
    #calling the functions

#functions
def red3(a):
    for i in range(a):
        red=win.create_oval(70,40,130,100, fill="red")
        tk.update()
        time.sleep(0.05)
def redb3(a):
    for i in range(a):
        red=win.create_oval(70,40,130,100, fill="black")
        tk.update()
        time.sleep(0.05)
def amber3(a):
    for i in range(a):
        amber=win.create_oval(70,120,130,180, fill="orange")
        tk.update()
        time.sleep(0.05)
def amberb3(a):
    for i in range(a):
        amber=win.create_oval(70,120,130,180, fill="black")
        tk.update()
        time.sleep(0.05)
def green3(a):
    for i in range(a):
        green=win.create_oval(70,200,130,260, fill="green")
        tk.update()
        time.sleep(0.05)
def greenb3(a):
    for i in range(a):
        green=win.create_oval(70,200,130,260, fill="black")
        tk.update()
        time.sleep(0.05)
def lights3():
    red=win.create_oval(70,40,130,100, fill="black")
    amber=win.create_oval(70,120,130,180, fill ="black")
    green=win.create_oval(70,200,130,260, fill="black")
    #end of functions
    #calling the functions
    
lights()
red(30)
redb(1)
amber(10)
amberb(1)
green(30)
greenb(1)

lights1()
red1(30)
redb1(1)
amber1(10)
amberb1(1)
green1(30)
greenb1(1)

lights2()
red2(30)
redb2(1)
amber2(10)
amberb2(1)
green2(30)
greenb2(1)

lights3()
red3(30)
redb3(1)
amber3(10)
amberb3(1)
green3(30)
greenb3(1)

tk.mainloop()