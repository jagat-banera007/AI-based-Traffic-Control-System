# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 19:48:51 2022

@author: JAGAT
"""
import time 
from tkinter import *
from tkinter import messagebox

class TrafficLights:

    def __init__(self,lane):

        window = Tk()
        window.title("Opening Lane " + str(lane) + "....")
       


        frame = Frame(window)
        frame.pack()

        self.color = StringVar()

        '''radio_red = Radiobutton(frame, text="Red", bg="red", variable=self.color, value="R", command=self.on_RadioChange)
        radio_red.grid(row=10, column=1)

        radio_yellow = Radiobutton(frame, text="Yellow", bg="yellow", variable=self.color, value="Y", command=self.on_RadioChange)               
        radio_yellow.grid(row = 10, column = 2)

        radio_green = Radiobutton(frame, text="Green", bg="green", variable=self.color, value="G", command=self.on_RadioChange)
        radio_green.grid(row = 10, column = 3)'''
        '''self.canvas_message = Canvas(window, width=100, height=50, bg="black")
        time.sleep(2)
        self.canvas_message.create_text(10, 25, text="Opening Lane " + str(lane)+"....", fill="cyan", font=('Helvetica 15 bold'))
        self.canvas_message.destroy()'''
        self.canvas = Canvas(window, width=500, height=480, bg="black")
        self.canvas.pack()
        self.canvas.create_text(70, 40, text="LANE 1", fill="cyan", font=('Helvetica 15 bold'))
        self.canvas.create_text(190, 40, text="LANE 2", fill="cyan", font=('Helvetica 15 bold'))
        self.canvas.create_text(310, 40, text="LANE 3", fill="cyan", font=('Helvetica 15 bold'))
        self.canvas.create_text(430, 40, text="LANE 4", fill="cyan", font=('Helvetica 15 bold'))
        
        if lane == 1 :
            self.oval_red_1 = self.canvas.create_oval(20, 70, 120, 170, fill="white")
            self.oval_yellow_1 = self.canvas.create_oval(20, 190, 120, 290, fill="white")
            self.oval_green_1 = self.canvas.create_oval(20, 310, 120, 410, fill="green")
        
            self.oval_red_2 = self.canvas.create_oval(140, 70, 240, 170, fill="red")
            self.oval_yellow_2 = self.canvas.create_oval(140, 190, 240, 290, fill="white")
            self.oval_green_2 = self.canvas.create_oval(140, 310, 240, 410, fill="white")
            
            self.oval_red_3 = self.canvas.create_oval(260, 70, 360, 170, fill="red")
            self.oval_yellow_3 = self.canvas.create_oval(260, 190, 360, 290, fill="white")
            self.oval_green_3 = self.canvas.create_oval(260, 310, 360, 410, fill="white")
            
            self.oval_red_4 = self.canvas.create_oval(380, 70, 480, 170, fill= "red")
            self.oval_yellow_4 = self.canvas.create_oval(380,190, 480, 290, fill="white")
            self.oval_green_4 = self.canvas.create_oval(380, 310, 480, 410, fill="white")
            
        
        
        if lane == 2 :
            self.oval_red_1 = self.canvas.create_oval(20, 70, 120, 170, fill="red")
            self.oval_yellow_1 = self.canvas.create_oval(20, 190, 120, 290, fill="white")
            self.oval_green_1 = self.canvas.create_oval(20, 310, 120, 410, fill="white")
        
            self.oval_red_2 = self.canvas.create_oval(140, 70, 240, 170, fill="white")
            self.oval_yellow_2 = self.canvas.create_oval(140, 190, 240, 290, fill="white")
            self.oval_green_2 = self.canvas.create_oval(140, 310, 240, 410, fill="green")
            
            self.oval_red_3 = self.canvas.create_oval(260, 70, 360, 170, fill="red")
            self.oval_yellow_3 = self.canvas.create_oval(260, 190, 360, 290, fill="white")
            self.oval_green_3 = self.canvas.create_oval(260, 310, 360, 410, fill="white")
            
            self.oval_red_4 = self.canvas.create_oval(380, 70, 480, 170, fill= "red")
            self.oval_yellow_4 = self.canvas.create_oval(380,190, 480, 290, fill="white")
            self.oval_green_4 = self.canvas.create_oval(380, 310, 480, 410, fill="white")
            
            
            
        if lane == 3 :
            self.oval_red_1 = self.canvas.create_oval(20, 70, 120, 170, fill="red")
            self.oval_yellow_1 = self.canvas.create_oval(20, 190, 120, 290, fill="white")
            self.oval_green_1 = self.canvas.create_oval(20, 310, 120, 410, fill="white")
        
            self.oval_red_2 = self.canvas.create_oval(140, 70, 240, 170, fill="red")
            self.oval_yellow_2 = self.canvas.create_oval(140, 190, 240, 290, fill="white")
            self.oval_green_2 = self.canvas.create_oval(140, 310, 240, 410, fill="white")
            
            self.oval_red_3 = self.canvas.create_oval(260, 70, 360, 170, fill="white")
            self.oval_yellow_3 = self.canvas.create_oval(260, 190, 360, 290, fill="white")
            self.oval_green_3 = self.canvas.create_oval(260, 310, 360, 410, fill="green")
            
            self.oval_red_4 = self.canvas.create_oval(380, 70, 480, 170, fill= "red")
            self.oval_yellow_4 = self.canvas.create_oval(380,190, 480, 290, fill="white")
            self.oval_green_4 = self.canvas.create_oval(380, 310, 480, 410, fill="white")
            
            
        if lane == 4 :
            self.oval_red_1 = self.canvas.create_oval(20, 70, 120, 170, fill="red")
            self.oval_yellow_1 = self.canvas.create_oval(20, 190, 120, 290, fill="white")
            self.oval_green_1 = self.canvas.create_oval(20, 310, 120, 410, fill="white")
        
            self.oval_red_2 = self.canvas.create_oval(140, 70, 240, 170, fill="red")
            self.oval_yellow_2 = self.canvas.create_oval(140, 190, 240, 290, fill="white")
            self.oval_green_2 = self.canvas.create_oval(140, 310, 240, 410, fill="white")
            
            self.oval_red_3 = self.canvas.create_oval(260, 70, 360, 170, fill="red")
            self.oval_yellow_3 = self.canvas.create_oval(260, 190, 360, 290, fill="white")
            self.oval_green_3 = self.canvas.create_oval(260, 310, 360, 410, fill="white")
            
            self.oval_red_4 = self.canvas.create_oval(380, 70, 480, 170, fill= "white")
            self.oval_yellow_4 = self.canvas.create_oval(380,190, 480, 290, fill="white")
            self.oval_green_4 = self.canvas.create_oval(380, 310, 480, 410, fill="green")
        


        #self.color.set('R')
        #self.canvas.itemconfig(self.oval_red, fill="white")

        window.mainloop()

    
TrafficLights(4)