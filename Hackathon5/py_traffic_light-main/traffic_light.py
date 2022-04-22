#!/usr/bin/env python3

from tkinter import Canvas

#a class for a traffic light widget

class TrafficLight(Canvas):

    #define which lamp names exist
    #these are ordered from top to bottom
    LAMP_NAMES = ("red", "yellow", "green")

    #define the default diameter of lamps
    #the size of the widget overall is
    #also derived from this
    LAMP_SIZE = 25

    #define the colors of each lamp by name
    #also define a default color for when the
    #lamps are turned off (this is the same for all three)
    LAMP_COLORS = {
        "red"       : "#FF0000",
        "yellow"    : "#FFFF00",
        "green"     : "#00FF00",
        "default"   : "#000000"
        }


    #internal method 
    #draws the lamps on the internal canvas according to LAMP_ORDER and LAMP_SIZE
    def _placeLamps(self):
        #retrieve the default color so 
        #the lamps can be filled with it
        defaultColor = self.LAMP_COLORS["default"]
        
        #previousY1 is initialized to 1 so the fist lamp
        #doesn't touch the top of the canvas 
        previousY1 = 1
        
        #create and position the lamps
        #store each lamp's id in the self.lampIds dict
        #with the appropriate color as the key
        for lampName in self.LAMP_NAMES:
            #calculate bounding box coordinates
            x0 = 2 #left side set to 2; this ensures the left side doesn't touch the border
            y0 = previousY1 + 2 #top of this lamp is 2px below the bottom of the previous one
            x1 = x0 + self.LAMP_SIZE #right side of the lamp is <lampSize> px to the right of the left side
            y1 = y0 + self.LAMP_SIZE #bottom of this lamp is <lampSize> px below the top
            
            #use calculated coordinates to draw the lamp (with the default color as the fill)
            self.lampIds[lampName] = self.create_oval(x0, y0, x1, y1, fill=defaultColor)
            #set previousY1 to the y1 just used
            previousY1 = y1


    def __init__(self, parent):

        #run superclass constructor with defined width, height, and bg color
        Canvas.__init__(self, 
            parent, 
            width=TrafficLight.LAMP_SIZE+3, 
            height=(TrafficLight.LAMP_SIZE+3)*3, 
            background="#FFFFFF"
            )
        
        #store parent
        self.parent = parent

        #create a dict to store lamp ids
        #this is created from the defined lamp order;
        #modify TrafficLight.LAMP_ORDER to change what 
        #lamps are available
        self.lampIds = dict.fromkeys(self.LAMP_NAMES, None)

        #draw lamps and store their ids in self.lampIds
        self._placeLamps()

        #end __init__


    #given a lamp color ("red", "yellow", or "green"),
    #"turns the lamp on" by setting its fill color
    def turnLampOn(self, lampColor):
        lampId = self.lampIds[lampColor]
        colorStr = self.LAMP_COLORS[lampColor]
        self.itemconfigure(lampId, fill=colorStr)


    #similar to self.turnLampOn, but turns the lamp off
    #by setting it to the default color
    def turnLampOff(self, lampColor):
        lampId = self.lampIds[lampColor]
        colorStr = self.LAMP_COLORS["default"]
        self.itemconfigure(lampId, fill=colorStr)


    #returns True if the selected lamp is currently
    #turned on, False if it is turned off
    def isLampOn(self, lampColor):
        lampId = self.lampIds[lampColor]
        currentLampColor = self.itemcget(lampId, 'fill')
        #if the current lamp color is not the default color, 
        #then the lamp must be on; otherwise, the lamp is turned off
        #because this evaluates to a boolean, it can be returned directly
        return (currentLampColor != self.LAMP_COLORS["default"])


    #returns an iterator of lamp names ("red", "yellow", "green")
    #"containing" the names of every lamp that is currently turned on
    #if asList is true, returns a list rather than an iterator
    def getActiveLamps(self, asList = False):
        activeLampsIterator = filter(self.isLampOn, self.LAMP_NAMES)
        if not asList:
            return activeLampsIterator
        else:
            return list(activeLampsIterator)


    #turns the selected lamp on, and also
    #turns all other lamps off
    #if lampColor is None, all lamps are turned off
    def setActiveLamp(self, lampColor = None):

        #turn off all currently active lamps
        for activeLamp in self.getActiveLamps():
            self.turnLampOff(activeLamp)
        
        if lampColor != None:
            #turn the selected lamp on
            self.turnLampOn(lampColor)


    #returns the name of the lamp that is directly 
    #after the currently active lamp (ordering top to bottom)
    #if no lamps are active, returns the first lamp
    #if the last lamp is active, returns None
    #if multiple lamps are active, only the first is considered
    def getNextLamp(self):
         #get a list of all currently active lamps
        activeLamps = self.getActiveLamps(asList=True)
        
        #if no lamps are active, return the first lamp
        if len(activeLamps) == 0:
            return TrafficLight.LAMP_NAMES[0]
        else:
            #if at least one lamp is active, treat the first
            #active lamp as the only active lamp
            activeLamp = activeLamps[0]
            
            #if the active lamp is the last lamp, 
            #return None 
            if activeLamp == TrafficLight.LAMP_NAMES[-1]:
                return None
            
            #otherwise, find the currently active lamp's index,
            #add 1, then turn that lamp's name
            else:
                lampIndex = TrafficLight.LAMP_NAMES.index(activeLamp)
                nextLamp = TrafficLight.LAMP_NAMES[lampIndex + 1]
                return nextLamp


    #increments the state of this traffic light
    #that is, turns the current lamp off and 
    #turns the next lamp on ("next lamp" being defined
    # by the self.getNextLamp function)
    def incrementState(self):
        nextLamp = self.getNextLamp()
        self.setActiveLamp(nextLamp)
       

#end TrafficLight 

if __name__ == "__main__":
    print("This is a class definition used as part of a larger script")
    print("Did you mean to run py_traffic_light.py?")