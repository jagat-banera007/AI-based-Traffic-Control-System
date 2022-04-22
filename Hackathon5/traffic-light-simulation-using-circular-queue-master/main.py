from tkinter import *
from tkinter import ttk
from functools import partial
from tkinter import messagebox
import time
import sys
from datetime import date
sys.setrecursionlimit(1500)
########################################################################
n=4
r1=-1
f1=-1
list1=[0,0,0,0]
root = Tk()
#root.attributes("-fullscreen", True)
########################################################################################

def qInsert1(list1,element):
    global n, r1, f1
    if r1==-1 and f1==-1:
        r1=0
        f1=0
    elif r1==n-1:
        r1=0
    else:
        r1=r1+1
    list1[r1]=element

def qDelete1(list1):
    global r1, f1, n
    if r1==f1:
        r1=-1
        f1=-1
    elif f1==n-1:
        f1=0
    else:
        f1=f1+1

def initialFill(list1,g):
    qInsert1(list1, ["GREEN",g])
    qInsert1(list1, ["RED",g+5])
    qInsert1(list1, ["RED",2*(g+5)])
    qInsert1(list1, ["RED",3*(g+5)])

##############################################################################

g2=0
autoModeState=0
stopState=0
resetState=0
breakerValue=0
sig = [0, 0, 0, 0]
tLab = [0, 0, 0, 0]
pattern = ' {0:02d} '
pic1 = PhotoImage(file="pics/sample.png")
pic2 = PhotoImage(file="pics/sample2.png")
pic3 = PhotoImage(file="pics/sample3.png")
pic4 = PhotoImage(file="pics/sample4.png")
bimg3=PhotoImage(file="pics/4a.png")
bimg4=PhotoImage(file="pics/5a.png")
bimg5=PhotoImage(file="pics/6a.png")

def initialImageSet():
    global pic1, pic2, sig
    sig[0].config(image=pic1)
    sig[1].config(image=pic2)
    sig[2].config(image=pic2)
    sig[3].config(image=pic2)

def getColor(labelA,labelB,labelC,labelD,pic):
    labelA.config(image=pic)
    labelB.config(image=pic)
    labelC.config(image=pic)
    labelD.config(image=pic)

def flashColor(labelA,labelB,labelC,labelD,pic,off,i):
    global breakerValue
    if breakerValue==1:
        labelA.config(image=off)
        labelB.config(image=off)
        labelC.config(image=off)
        labelD.config(image=off)
        return
    if i%2==0 and i<100000:
        labelA.config(image=off)
        labelB.config(image=off)
        labelC.config(image=off)
        labelD.config(image=off)
        i=i+1
        root.after(350,getColor,labelA,labelB,labelC,labelD,pic)
        root.after(650, flashColor, labelA,labelB,labelC,labelD,pic,off,i)
    elif i%2!=0 and i<100000:
        labelA.config(image=pic)
        labelB.config(image=pic)
        labelC.config(image=pic)
        labelD.config(image=pic)
        i = i + 1
        root.after(350,getColor,labelA,labelB,labelC,labelD,off)
        root.after(650, flashColor, labelA,labelB,labelC,labelD,pic,off, i)

autoOnNight=0
autoOnDay=0
def nightChecker():
    global time1, pic1, pic2, pic3, pic4, sig, root, autoOnNight, list1, autoOnDay, g2, root, resetState,autoModeState, timeSlab1, timeSlab2
    if resetState==1:
        autoOnNight = 0
        autoOnDay = 0
        autoModeState = 0
        sig[0].config(image=pic4)
        sig[1].config(image=pic4)
        sig[2].config(image=pic4)
        sig[3].config(image=pic4)
        tLab[0].config(text=" 00 ")
        tLab[1].config(text=" 00 ")
        tLab[2].config(text=" 00 ")
        tLab[3].config(text=" 00 ")
        return
    elif ((int(time1[0]+time1[1]) >= timeSlab2) or (int(time1[0]+time1[1])<timeSlab1 and int(time1[0]+time1[1])>=0)) and autoOnNight==0:
        autoOnNight=1
        autoOnDay=0
        sig[0].config(image=pic3)
        sig[1].config(image=pic3)
        sig[2].config(image=pic3)
        sig[3].config(image=pic3)
        tLab[0].config(text=" 00 ")
        tLab[1].config(text=" 00 ")
        tLab[2].config(text=" 00 ")
        tLab[3].config(text=" 00 ")
        qDelete1(list1)
    elif (int(time1[0]+time1[1])>=timeSlab1) and int(time1[0]+time1[1])<timeSlab2 and autoOnDay==0:
        autoOnDay=1
        qDelete1(list1)
        initialFill(list1,g2)
        initialImageSet()
        if autoOnDay==1:
            root.after(1000,afterStart)
    if autoModeState==1:
        root.after(1000, nightChecker)
def autoMode():
    global buttonStart, buttonNight, buttonAuto, g2, list1, autoModeState, resetState, timeSlab1, timeSlab2, t1, t2, root
    autoModeState=1
    resetState=0
    timeSlab1 = int(t1.get())
    timeSlab2 = int(t2.get())
    if not((timeSlab1>=6 and timeSlab1<=11) and (timeSlab2>=17 and timeSlab2<=23)):
        messagebox.showinfo("Invalid Input", "Time out of range. Enter 'On Time' between 6 to 11 and 'Off Time' between 17 to 23")
        return
    buttonStart.config(state=DISABLED)
    buttonNight.config(state=DISABLED)
    buttonAuto.config(state=DISABLED)
    g2=25
    root.after(1000,nightChecker)
def afterStartNight():
    global root, pic3, pic4, sig, tLab, n, i
    flashColor(sig[0],sig[1],sig[2],sig[3],pic3, pic4, 0)

def f5():
    global buttonNight, buttonStart, breakerValue, buttonAuto, nightRunning
    buttonNight.config(state=DISABLED)
    buttonStart.config(state=DISABLED)
    buttonAuto.config(state=DISABLED)
    breakerValue=0
    nightRunning=1
    afterStartNight()
def f6():
    global breakerValue, nightRunning
    nightRunning=0
    breakerValue=1
    buttonNight.config(state=NORMAL)
    buttonStart.config(state=NORMAL)


def afterStart():
    global root, pic1, pic2, pic3, pic4, state, sig, tLab, list1, n, g2, resetState, autoOnDay
    if resetState==1:
        return
    if autoOnDay==0 and autoModeState==1:
        for i in range(1, n + 1):
            qDelete1(list1)
        initialFill(list1, g2)
        tLab[0].config(text=" 00 ")
        tLab[1].config(text=" 00 ")
        tLab[2].config(text=" 00 ")
        tLab[3].config(text=" 00 ")
        return

    for i in range(0,n):
        if list1[i][0]=="GREEN" and list1[i][1]==0:
            sig[i].config(image=pic3)
            list1[i][0] = "YELLOW"
            list1[i][1]=5
        elif list1[i][0]=="YELLOW" and list1[i][1]==0:
            sig[i].config(image=pic2)
            list1[i][0]="RED"
            list1[i][1]=(3*(int(g2)+5))
            if i==3:
                sig[0].config(image=pic1)
                list1[0][0] = "GREEN"
                list1[0][1]=int(g2)
            else:
                sig[i+1].config(image=pic1)
                list1[i+1][0] = "GREEN"
                list1[i+1][1]=int(g2)
    for k in range(0,n):
        list1[k][1] -=1
        timeString = pattern.format(list1[k][1])
        tLab[k].config(text=timeString)
    if resetState==1:
        for i in range(1, n + 1):
            qDelete1(list1)
        initialFill(list1, g2)
        tLab[0].config(text=" 00 ")
        tLab[1].config(text=" 00 ")
        tLab[2].config(text=" 00 ")
        tLab[3].config(text=" 00 ")
        sig[0].config(image=pic4)
        sig[1].config(image=pic4)
        sig[2].config(image=pic4)
        sig[3].config(image=pic4)
        return
    else:
        root.after(1000, afterStart)

#opens rootlation window
def f3():
    global tLab, state, g2, g1, list1, buttonStart, root, pattern, resetState, buttonNight, buttonAuto
    g2=int(g1.get())
    if g2>40 or g2<10:
        messagebox.showinfo("Invalid Input", "Time out of range. Enter value between 10 and 50")
        return
    resetState = 0
    initialFill(list1, g2)
    buttonNight.config(state=DISABLED)
    buttonAuto.config(state=DISABLED)
    initialImageSet()
    tLab[0].config(text=pattern.format(list1[0][1]))
    tLab[1].config(text=pattern.format(list1[1][1]))
    tLab[2].config(text=pattern.format(list1[2][1]))
    tLab[3].config(text=pattern.format(list1[3][1]))
    buttonStart.config(state=DISABLED)
    root.after(1000, afterStart)
def f4():
    global autoOnNight, autoOnDay, autoModeState
    global resetState, state, n, tLab, sig, list1, buttonStart, labelB, greenTimeInput, nightRunning, buttonNight, breakerValue, buttonAuto
    buttonAuto.config(state=NORMAL)
    buttonStart.config(state=NORMAL)
    buttonNight.config(state=NORMAL)
    resetState=1
    if breakerValue==0:
        f6()
    qDelete1(list1)
    qDelete1(list1)
    qDelete1(list1)
    qDelete1(list1)
    tLab[0].config(text=" 00 ")
    tLab[1].config(text=" 00 ")
    tLab[2].config(text=" 00 ")
    tLab[3].config(text=" 00 ")
    greenTimeInput.config(state=NORMAL)
    sig[0].config(image=pic4)
    sig[1].config(image=pic4)
    sig[2].config(image=pic4)
    sig[3].config(image=pic4)
screenButton=0
screenStatus=0
inScreen = PhotoImage(file="pics/in.png")
outScreen = PhotoImage(file="pics/out.png")
def fullScreenEnter(window):
    global screenButton, inScreen, screenStatus
    screenStatus=1
    window.attributes("-fullscreen", True)
    screenButton.config(image=inScreen)
def fullScreenExit(window):
    global screenStatus, outScreen, screenButton
    screenStatus=0
    window.attributes("-fullscreen", False)
    screenButton.config(image=outScreen)
def fullScreenManager(window):
    global screenButton, screenStatus, inScreen, outScreen
    if screenStatus==0:
        fullScreenEnter(window)
    else:
        fullScreenExit(window)

def back10a():
    global button10a, g1, sig, tLab, pic1, pic2, pic3, pic4, pattern, buttonStart, labelB, sidebar, mainarea
    win2Destroyer()

def win2Destroyer():
    global designLab, backButton1a, newPic, labelNew, bimg1, bimg2, bimg3, bimg4, bimg5, bimg6, button1, button2, screenButton, mainButtonPic, rootButton, w, h
    global g1, sig, tLab, pic1, pic2, pic3, pic4, pattern, buttonStart, labelB, sidebar, mainarea, tLab, state, g2, g1, list1, buttonStart, root
    global pattern, resetState, buttonNight, buttonAuto, timeGetter1, timeGetter2

    f3()
    sidebar.destroy()
    mainarea.destroy()
    tLab[0].destroy()
    tLab[1].destroy()
    tLab[2].destroy()
    tLab[3].destroy()

    newPic = PhotoImage(file="pics/4.png")
    labelNew = Label(root, image=newPic)
    labelNew.pack()
    # button images location -----START
    bimg1 = PhotoImage(file="pics/2.png")
    bimg2 = PhotoImage(file="pics/3.png")
    bimg3 = PhotoImage(file="pics/4a.png")
    bimg4 = PhotoImage(file="pics/5a.png")
    bimg5 = PhotoImage(file="pics/6a.png")
    bimg6 = PhotoImage(file="pics/7a.png")
    # button images location -----END

    # menu buttons on bottom left of root
    button1 = Button(root, text="", relief=GROOVE, command=codeShow, image=bimg1, borderwidth=0, highlightthickness=0)
    button1.place(x=(w / 3 + w / 16), y=h / 3 + 150)  # Pseudocode button
    button2 = Button(root, text="", relief=GROOVE, image=bimg2, command=designShow, borderwidth=0, highlightthickness=0)
    button2.place(x=(w / 3 + w / 12), y=h / 3 + 280)  # Design button

    # This button opens main rootlation window "root"
    mainButtonPic = PhotoImage(file="pics/1.png")
    rootButton = Button(root, image=mainButtonPic, relief=GROOVE, borderwidth=0, highlightthickness=0, command=win2)
    rootButton.place(x=(w / 3 + w / 12), y=h / 3)
    screenButton = Button(root, image=outScreen, command=partial(fullScreenManager, root))
    screenButton.place(x=10, y=h - h / 7)


def win2():
    global root, g1, t1, t2, sig, tLab, pic1, pic2, pic3, pic4, pattern, buttonStart, labelB, sidebar, mainarea, w, h
    global labelC, greenTimeInput, button10a, pic10a, whiteSpace
    global buttonStart, buttonReset, buttonNight, buttonAuto, time1, timeGetter1, timeGetter2

    mainDestroyer()
    g1 = StringVar()
    t1 = StringVar()
    t2 = StringVar()
    # sidebar
    sidebar = Frame(root, bg='#031016', height=h, relief='sunken', borderwidth=2)
    sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

    # main content area
    mainarea = Frame(root, bg="white", width=500, height=500)
    mainarea.pack(expand=True, fill='both', side='right')

    pic10a=PhotoImage(file="pics/10a.png")
    button10a=Button(sidebar,image=pic10a,border=0,highlightthickness=0,command=back10a)
    button10a.pack(anchor=NW,pady=10,padx=5)
    whiteSpace=Label(sidebar, text=" ", bg="#031016")
    whiteSpace.pack(padx=135)
    labelC = Label(sidebar, font=("Helvetica", 16), fg="white", text="Green Signal Time", bg="#031016")
    labelC.pack(pady=0)
    greenTimeInput = Spinbox(sidebar, fg="white", bg="#2b2b2b", font=("Helvetica", 14), from_=10, to=40, width=12,textvariable=g1)
    greenTimeInput.pack(pady=20)

    buttonStart = Button(sidebar, image=bimg3, command=f3, borderwidth=0, highlightthickness=0)
    buttonStart.pack(pady=10)
    buttonReset = Button(sidebar, image=bimg4, command=f4, borderwidth=0, highlightthickness=0)
    buttonReset.pack(pady=10)

    buttonNight = Button(sidebar, image=bimg5, command=f5, borderwidth=0, highlightthickness=0)
    buttonNight.pack(pady=10)

    Label(sidebar,font=("Helvetica", 16),text="On Time (AM)",bg="#031016",fg="white").pack(pady=5)
    timeGetter1 = Spinbox(sidebar, fg="white", bg="#2b2b2b", font=("Helvetica", 14), from_=6, to=11, width=10,textvariable=t1)
    timeGetter1.pack(pady=5)
    Label(sidebar,bg="#031016").pack(pady=5)
    Label(sidebar,font=("Helvetica", 16), text="Off Time (PM)",bg="#031016", fg="white").pack(pady=5)
    timeGetter2 = Spinbox(sidebar,fg="white", bg="#2b2b2b", font=("Helvetica", 14), from_=17, to=23, width=10,textvariable=t2)
    timeGetter2.pack(pady=5)

    buttonAuto = Button(sidebar,command=autoMode, image=bimg6, borderwidth=0, highlightthickness=0)
    buttonAuto.pack(pady=10)

    time1 = ''
    clock = Label(sidebar, font=('times', 20, 'bold'), bg="red", fg="white")
    clock.pack(pady=10)

    def tick():
        global time1, time2
        time2 = time.strftime('%H:%M:%S')
        if time2 != time1:
            time1 = time2
            clock.config(text=time2)
        clock.after(200, tick)
    tick()


    # frame=Frame(root,width=w,height=h/4).place(x=0,y=h/4)
    sig[0] = Label(mainarea, text="text", image=pic4, borderwidth=0)
    sig[0].place(x=w / 3.5, y=h / 170)
    sig[1] = Label(mainarea, text="text", image=pic4, borderwidth=0)
    sig[1].place(x=w / 1.9, y=h / 4)
    sig[2] = Label(mainarea, text="text", image=pic4, borderwidth=0)
    sig[2].place(x=w / 3.5, y=3 * h / 5 - h / 15)
    sig[3] = Label(mainarea, text="text", image=pic4, borderwidth=0)
    sig[3].place(x=w / 20, y=h / 4)

    tLab[0] = Label(root, text=" 00 ", font=("Helvetica", 18), bg="black", fg="red")
    tLab[1] = Label(root, text=" 00 ", font=("Helvetica", 18), bg="black", fg="red")
    tLab[2] = Label(root, text=" 00 ", font=("Helvetica", 18), bg="black", fg="red")
    tLab[3] = Label(root, text=" 00 ", font=("Helvetica", 18), bg="black", fg="red")
    tLab[0].place(x=w / 1.8, y=h / 170 + 230)
    tLab[1].place(x=3 * w / 4 + w / 22, y=h / 4 + 238)
    tLab[2].place(x=w / 1.8, y=4.2 * h / 5)
    tLab[3].place(x=w / 4 + w / 14, y=h / 4 + 238)

##############################################################################

###############################################
root.state("zoomed")
#root is the main container

#This extracts screen resolution
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#iconbitmap is used adding icon in the title bar of the root window
root.iconbitmap(r'pics/titleIcon.ico')

def designShowDestroyer():
    global designLab, backButton1a
    designLab.destroy()
    backButton1a.destroy()

def codeShowDestroyer():
    global codeFrame, codeCanvas, scroll_y
    codeCanvas.destroy()
    scroll_y.destroy()

def mainDestroyer():
    global labelNew, button1, button2, rootButton, screenButton
    labelNew.destroy()
    button1.destroy()
    button2.destroy()
    rootButton.destroy()
    screenButton.destroy()
def backFunc1a():
    global designLab, backButton1a, newPic, labelNew, bimg1, bimg2, bimg3, bimg4, bimg5, bimg6, button1, button2, screenButton, mainButtonPic, rootButton, w, h

    designShowDestroyer()
    newPic = PhotoImage(file="pics/4.png")
    # root.config(image=newPic)
    # headPic=PhotoImage(file="pics/header.png")
    # header=Label(root,image=headPic)
    # header.place(x=0,y=0)
    labelNew = Label(root, image=newPic)
    labelNew.pack()
    # button images location -----START
    bimg1 = PhotoImage(file="pics/2.png")
    bimg2 = PhotoImage(file="pics/3.png")
    bimg3 = PhotoImage(file="pics/4a.png")
    bimg4 = PhotoImage(file="pics/5a.png")
    bimg5 = PhotoImage(file="pics/6a.png")
    bimg6 = PhotoImage(file="pics/7a.png")
    # button images location -----END

    # menu buttons on bottom left of root
    button1 = Button(root, text="", relief=GROOVE, command=codeShow, image=bimg1, borderwidth=0, highlightthickness=0)
    button1.place(x=(w / 3 + w / 16), y=h / 3 + 150)  # Pseudocode button
    button2 = Button(root, text="", relief=GROOVE, image=bimg2, command=designShow, borderwidth=0, highlightthickness=0)
    button2.place(x=(w / 3 + w / 12), y=h / 3 + 280)  # Design button

    # This button opens main rootlation window "root"
    mainButtonPic = PhotoImage(file="pics/1.png")
    rootButton = Button(root, image=mainButtonPic, relief=GROOVE, borderwidth=0, highlightthickness=0, command=win2)
    rootButton.place(x=(w / 3 + w / 12), y=h / 3)
    screenButton = Button(root, image=outScreen, command=partial(fullScreenManager, root))
    screenButton.place(x=10, y=h - h / 7)

def backFunc2a():
    global root, codeCanvas, codeFrame, backButton1a, newPic, labelNew, bimg1, bimg2, bimg3, bimg4, bimg5, bimg6, button1, button2, screenButton, mainButtonPic, rootButton, scroll_y, w, h

    codeShowDestroyer()
    newPic = PhotoImage(file="pics/4.png")
    # root.config(image=newPic)
    # headPic=PhotoImage(file="pics/header.png")
    # header=Label(root,image=headPic)
    # header.place(x=0,y=0)
    labelNew = Label(root, image=newPic)
    labelNew.pack()
    # button images location -----START
    bimg1 = PhotoImage(file="pics/2.png")
    bimg2 = PhotoImage(file="pics/3.png")
    bimg3 = PhotoImage(file="pics/4a.png")
    bimg4 = PhotoImage(file="pics/5a.png")
    bimg5 = PhotoImage(file="pics/6a.png")
    bimg6 = PhotoImage(file="pics/7a.png")
    # button images location -----END

    # menu buttons on bottom left of root
    button1 = Button(root, text="", relief=GROOVE, command=codeShow, image=bimg1, borderwidth=0, highlightthickness=0)
    button1.place(x=(w / 3 + w / 16), y=h / 3 + 150)  # Pseudocode button
    button2 = Button(root, text="", relief=GROOVE, image=bimg2, command=designShow, borderwidth=0, highlightthickness=0)
    button2.place(x=(w / 3 + w / 12), y=h / 3 + 280)  # Design button

    # This button opens main rootlation window "root"
    mainButtonPic = PhotoImage(file="pics/1.png")
    rootButton = Button(root, image=mainButtonPic, relief=GROOVE, borderwidth=0, highlightthickness=0, command=win2)
    rootButton.place(x=(w / 3 + w / 12), y=h / 3)
    screenButton = Button(root, image=outScreen, command=partial(fullScreenManager, root))
    screenButton.place(x=10, y=h - h / 7)

# opens window with program design
backPic=PhotoImage(file="pics/9a.png")
def designShow():
    global labelNew, button1, button2, rootButton, screenButton, backPic, w, h, designLab, root, backButton1a, newPic, pic4, designPic2

    mainDestroyer()
    designPic2=PhotoImage(file="pics/designPic.png")
    designLab=Label(root,image=designPic2)
    designLab.pack()
    backButton1a=Button(root,image=backPic,border=0,highlightthickness=0,command=backFunc1a)
    backButton1a.place(x=25,y=30)

#opens window with pseudo code
def codeShow():
    global codePic1, codePic2, codePic3, codeCanvas, codeFrame, labelNew, button1, button2, rootButton, screenButton, backPic, w, h, designLab
    global root, backButton1a, newPic, pic4, designPic2, backPic, backButton2a, scroll_y

    mainDestroyer()
    codeCanvas = Canvas(root)
    codeFrame = Frame(codeCanvas)
    backButton2a=Button(root,image=backPic,border=0,highlightthickness=0,command=backFunc2a)
    backButton2a.place(x=20,y=30)
    codePic1=PhotoImage(file="pics/codePic1.png")
    codePic2 = PhotoImage(file="pics/codePic2.png")
    codePic3 = PhotoImage(file="pics/codePic3.png")

    scroll_y = Scrollbar(root, orient="vertical", command=codeCanvas.yview)
    # group of widgets
    codeLab1=Label(codeFrame,image=codePic1,highlightthickness=0,border=0)
    codeLab2 = Label(codeFrame, image=codePic2,highlightthickness=0,border=0)
    codeLab3 = Label(codeFrame, image=codePic3,highlightthickness=0,border=0)
    codeLab1.pack()
    codeLab2.pack()
    codeLab3.pack()

    codeCanvas.create_window(0, 0, anchor='nw', window=codeFrame)
    codeCanvas.update_idletasks()
    codeCanvas.configure(scrollregion=codeCanvas.bbox('all'),
                         yscrollcommand=scroll_y.set)

    codeCanvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')


root.geometry("%dx%d+0+0" % (w, h))
root.title("Simulator")

newPic=PhotoImage(file="pics/4.png")

labelNew=Label(root,image=newPic)
labelNew.pack()
#button images location -----START
bimg1=PhotoImage(file="pics/2.png")
bimg2=PhotoImage(file="pics/3.png")
bimg3=PhotoImage(file="pics/4a.png")
bimg4=PhotoImage(file="pics/5a.png")
bimg5=PhotoImage(file="pics/6a.png")
bimg6=PhotoImage(file="pics/7a.png")
#button images location -----END


#menu buttons on bottom left of root
button1=Button(root,text="",relief=GROOVE,command=codeShow,image=bimg1,borderwidth=0,highlightthickness=0)
button1.place(x=(w/3 + w/16),y=h/3 + 150 )#Pseudocode button
button2=Button(root,text="",relief=GROOVE,image=bimg2,command=designShow,borderwidth=0,highlightthickness=0)
button2.place(x=(w/3 + w/12),y=h/3 + 280)#Design button

#This button opens main rootlation window "root"
mainButtonPic=PhotoImage(file="pics/1.png")
rootButton=Button(root,image=mainButtonPic,relief=GROOVE,borderwidth=0,highlightthickness=0,command=win2)
rootButton.place(x=(w/3 + w/12),y=h/3)
screenButton=Button(root,image=outScreen,command=partial(fullScreenManager,root))
screenButton.place(x=10,y=h-h/7)
#sets the root window in focus
root.focus_force()

#program call
root.mainloop()