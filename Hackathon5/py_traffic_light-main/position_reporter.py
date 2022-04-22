#!/usr/bin/env python3

from typing import Tuple
from tkinter import Misc as BaseTkObject
#I import tkinter.Misc as BaseTkObject to be more representative of what it is;
#This is a personal preference and is by no means required
#(you may consider this bad form as there is another class
# in tkinter called BaseWidget already; as it happens that class
# already inherits )

#Position Reporter Interface
#An "interface" (implemented as an abstract class) 
#for rectangular things to report their current position and dimensions
#Descriptions of the expected behavior of each method can be found
#in the concrete PositionReporter definition
class PositionReporterInterface:

    _ERROR_MESSAGE_TEXT = "PositionReporterInterface is abstract and does not provide concrete method definitions"

    def getPos(self) -> Tuple[int, int]:
        raise NotImplementedError(PositionReporterInterface._ERROR_MESSAGE_TEXT)

    def getDimensions(self) -> Tuple[int, int]:
        raise NotImplementedError(PositionReporterInterface._ERROR_MESSAGE_TEXT)

    def getCorners(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        raise NotImplementedError(PositionReporterInterface._ERROR_MESSAGE_TEXT)


#Position Reporter
#A "concrete interface" (implemented as a mixin) for widgets to report their current position
#When I say "concrete interface", I mean that this class is to be used 
#in addition to a more useful base class (there may be a more proper word for this)

class PositionReporter(PositionReporterInterface, BaseTkObject):

    #override constructor to make PositionReporter a mixin class
    #*args and **kwargs capture any and all arguments passed to the
    #constructor of another class (PositionReporter itself doesn't
    #take any arguments in the constructor)
    def __init__(self, *args, **kwargs):

        #run the superclass constructor using 
        #all arguments that were passed
        super().__init__(*args, **kwargs)
        #if another class inherits from both
        #PositionReporter and another class then this call to 
        #super().__init__ will point to that second class
        #this is because tkinter.Misc (aka BaseTkObject) has no __init__ method
        #(I beleive it was designed as an interface similar to this one)

    #return coordinates within parent
    #as a 2-tuple (x, y)
    #adjusts for parent having a border
    #by default, if targetWidget is a PositionReporter instance,
    #then the targetWidget's getPos method will be used
    #setting forceStatic to True will disable this behavior
    #if targetWidget is not a PositionReporter, forceStatic has no effect
    #This behavior is common to all staticmethods and classmethods in this class definition
    @staticmethod
    def getPosOfWidget(targetWidget: BaseTkObject, forceStatic = False) -> Tuple[int, int]:

        #if forceStatic is false and the target is a PositionReporter,
        # use the target's getPos method
        if not forceStatic and isinstance(targetWidget, PositionReporter):
            return targetWidget.getPos()

        #get "base" (unadjusted) coordinates
        baseX = targetWidget.winfo_x()
        baseY = targetWidget.winfo_y()

        #get parent's border width
        parentBorderWidth = targetWidget.master.cget("borderwidth")

        #adjust coordinates and store in a tuple
        coordinates = (
            baseX - parentBorderWidth,
            baseY - parentBorderWidth
        )

        return coordinates
        
    
    #return the (x, y) coordinates of this widget
    #you can override this method to define custom 
    #corner-locating behavior on a class by class basis
    #(e.g. offsetting coordinates by a constant, rotating 
    #coordinates about an axis, translating to and 
    #from different coordinate spaces, etc)
    def getPos(self) -> Tuple[int,int]:

        #by default, getPos simply uses getPosOfWidget with forceStatic set to True 
        #(if forceStatic were False, getPosOfWidget would call getPos again and we
        # would be stuck in an infinite loop)
        return self.getPosOfWidget(self, forceStatic=True)

    #return the width and height of the specified widget
    #as a 2-tuple (width, height)
    #uses instancemethods if available; set forceStatic to True to disable this
    #see description of getPosOfWidget for more information on this behavior
    @staticmethod
    def getDimensionsOfWidget(targetWidget: BaseTkObject, forceStatic = False) -> Tuple[int, int]:

        if not forceStatic and isinstance(targetWidget, PositionReporter):
            return targetWidget.getDimensions()
        else:
            width = targetWidget.winfo_width()
            height = targetWidget.winfo_height()

            return (width, height)

    #overridable instancemethod version of getDimensionsOfWidget
    #see description of getPosOfWidget for a more detailed example
    #of this staticmethod + instancemethod pairing concept
    def getDimensions(self) -> Tuple[int, int]:
        return self.getDimensionsOfWidget(self, forceStatic=True)

    #return the x and y coordinates of the top left
    #and bottom right corners of the specified widget 
    #uses instancemethods if available; set forceStatic to True to disable this
    #see description of getPosOfWidget for more information on this behavior
    @classmethod
    def getCornersOfWidget(cls, targetWidget: BaseTkObject, forceStatic = False) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        
        #get top left corner and dimensions of widget
        #use instancemethods if forceStatic is False and targetWidget
        #is an instance of PositionReporter
        if not forceStatic and isinstance(targetWidget, PositionReporter):
            cornerTL = targetWidget.getPos()
            widgetWidth, widgetHeight = targetWidget.getDimensions()
        else:
            cornerTL = cls.getPosOfWidget(targetWidget)
            widgetWidth, widgetHeight = cls.getDimensionsOfWidget(targetWidget)
        
        #calculate the bottom right corner given the
        #widget's height and width
        cornerBR = (
            cornerTL[0] + widgetWidth,
            cornerTL[1] + widgetHeight
        )

        return (cornerTL, cornerBR)

    #return the x and y coordinates of the top left
    #and bottom right corners of this widget
    def getCorners(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.getCornersOfWidget(self)

#Rectangle
#A class that stores an origin and dimensions
#and exposes them using the PositionReporterInterface
class Rectangle(PositionReporterInterface):

    def __init__(self,
        originX: int or float,
        originY: int or float,
        width: int or float,
        height: int or float
        ):

        self.originX = originX
        self.originY = originY
        self.width = width
        self.height = height

    #return the origin coordinates
    def getPos(self) -> Tuple[int, int]:
        return (self.originX, self.originY)

    #return the dimensions
    def getDimensions(self) -> Tuple[int, int]:
        return (self.width, self.height)

    #return two 2-tuples representing the coordinates
    #of the top left and bottom right corners of this rectangle
    def getCorners(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        
        #top left corner is just the origin coordinates
        cornerTL = (self.originX, self.originY)

        #bottom right corner is origin coordinates
        #offset by the width and height
        cornerBR = (self.originX + self.width, self.originY + self.height)

        return (cornerTL, cornerBR)

    def __str__(self):
        return f"({repr(self.originX)}, {repr(self.originY)}, {repr(self.width)}, {repr(self.height)})"

    def __repr__(self):
        return "Rectangle"+self.__str__()