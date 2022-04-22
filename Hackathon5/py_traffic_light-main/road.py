#!/usr/bin/env python3

from tkinter import Canvas
from collider import Collider
from collision import Collision
from typing import Iterable, List, Tuple
from enum import Enum

#TrafficLineType
#an enum for the different kinds of traffic lines
class TrafficLineType(Enum):
    DASHED = "dashed"
    SOLID = "solid"


#A road widget drawn using the tkinter Canvas system
#Scales dynamically, and draws yellow lines down the center
#Detects intersections with other Roads and doesn't
#draw lines in the area of intersection
class Road(Collider, Canvas): 

    #define colors for elements of the road
    ROAD_COLOR = "#373B42"
    LINE_COLOR = "#FFFF00"

    #define the width of each traffic line
    #relative to the width of the Road
    LINE_WIDTH_PROPORTION = 1/32
    
    #define the height of each traffic line
    #relative to the width of that traffic line
    LINE_HEIGHT_PROPORTION = 4
    #note: this is only used for drawing dashed lines;
    #solid lines are unaffected by this

    #define the default line type that is used when
    #drawRoad is called without specifying a line type
    DEFAULT_LINE_TYPE = TrafficLineType.SOLID

    #given a TrafficLineType or a matching string,
    #returns a valid TrafficLineType
    #if the provided value is not a TrafficLineType or 
    #a string that matches one, a ValueError is raised
    @staticmethod
    def validateTrafficLineType(givenLineType):

        #if lineType is a TrafficLineType,
        #return it immediately
        if isinstance(givenLineType, TrafficLineType):
            return givenLineType

        #if lineType is a string,
        #check if that string is within TrafficLineType
        elif isinstance(givenLineType, str):
            #iterate through valid TrafficLineTypes
            for lineType in TrafficLineType:
                #check the value of each traffic light type
                #against the given line type
                if lineType.value == givenLineType:
                    #if a match is found, then return the matching TrafficLineType
                    return lineType
        
        #we can raise a ValueError unconditionally here because
        #the previous if statements would've already returned 
        #from this method if the givenLineType were valid
        errMsg = f"{givenLineType} is not a valid TrafficLineType!"
        raise ValueError(errMsg)


    #internal method
    #clears every object off the Canvas
    #this could apply to any Canvas subclass
    def _clearCanvas(self):
        allObjects = self.find_all()
        for object in allObjects:
            self.delete(object)

    #draws traffic lines down the middle of the widget
    #if clearBeforeDrawing param is True (default),
    #the widget will be entirely cleared before doing this
    #lineType specifies the type of lines to draw; if none is specified,
    #the _lineType of this Road is used by default. 
    #lineType must be a TrafficLineType or equivalent string
    def drawRoad(self, clearBeforeDrawing = True, lineType: TrafficLineType = None) -> bool:
        from math import ceil

        #clear canvas if not specified otherwise
        if clearBeforeDrawing:
            self._clearCanvas()

        if lineType == None:
            #use this Road's lineType if none was specified
            lineType = self._lineType
        else:
            #if a lineType was specified, validate it
            lineType = self.validateTrafficLineType(lineType)

        #alias width and height
        if not self.horizontal:
            currentWidth = self.currentWidth
            currentHeight = self.currentHeight
        else:
            #if this road is to be drawn horizontally,
            #swap width and height; this effectively swaps
            #the axis that calculations are based on
            currentHeight = self.currentWidth
            currentWidth = self.currentHeight

        #determine the size of one line segment
        #the width is the closest integer approximation of
        #the line width proportion multiplied by the width of the Road
        lineWidth = int(round(currentWidth * self.LINE_WIDTH_PROPORTION))

        #if line width is zero, return False to indicate failure
        if lineWidth == 0:
            #print("Cannot draw zero width line!")
            return False

        #init linesIterable to an empty list
        #this will be overwritten by one of 
        #the blocks of the following if statement
        linesIterable: Iterable[Tuple[int, int, int, int]] = []

        #get a sequence of lines to draw
        #the logic for this depends on the TrafficLineType
        #all will set the linesIterable to some Iterable 
        #filled with 4-tuples that describe each line to draw
        #(xOffset, yOffset, lineWidth, lineHeight)
        if lineType == TrafficLineType.SOLID:
            #Logic for solid traffic lines
            #roads with solid lines (at least here in the US) generally
            #have 2 solid lines in the center spaced apart by one line's width

            #the height of the lines is the same as the height of the road overall,
            #so there is no need to do any calculation for it
            #there also is no need to calculate a Y offset: as the lines 
            #will span the entire road, they all must start at y = 0

            #calculate the x offset for the left line
            #this is the closest integer approximation of
            #one half the Road's width minus 1 and 1 half (1.5 or 3/2) of the line's width
            #this puts the left line one half line's width to the left of center
            leftXOffset = int(round((currentWidth/2) - (lineWidth * 3/2)))

            #calculate the x offset for the right line
            #this is the left x offset plus the width of one line
            #since the left line is one half line to the left of
            #center, adding one line's width puts the right line
            #one half line's width to the right of center
            rightXOffset = leftXOffset + lineWidth

            #using these offsets, create a 2-tuple 
            #of two 4-tuples; one for each line
            #this tuple is used as the linesIterable
            #for the SOLID TrafficLineType
            linesIterable = (
                (leftXOffset, 0, lineWidth, currentHeight),
                (rightXOffset, 0, lineWidth, currentHeight)
                )
        
        elif lineType == TrafficLineType.DASHED:
            #Logic for dashed traffic lines
            #roads with dashed lines generally 
            #have them spaced one line's length apart

            #the height of one line segment is 4 times its width
            lineHeight = lineWidth * self.LINE_HEIGHT_PROPORTION

            #in order for the lines to be centered, they must
            #be offset to the right by a certain amount, shown here
            #integer approximation is used
            xOffset = int(round((currentWidth/2) - (lineWidth/2)))

            #determine the number of lines to draw
            #the line height is doubled to account for the space
            #between lines (the height of which is equal to the line height)
            #the result is rounded up to the nearest integer
            numberOfLines = ceil(currentHeight/(lineHeight*2))

            #calculate the inital space between the
            #top of the canvas and the top of the first line
            #line height is used twice here, the second usage is for the
            #space between lines
            initialYOffset = int(
                (currentHeight - (lineHeight * numberOfLines) - (lineHeight * (numberOfLines - 1))) / 2
                )
            #note: if the lines exceed the height of the canvas, this expression
            #will result in a negative value. this is fine, as this simply offsets
            #in the opposite direction (which still centers the lines)

            #define a generator function that will calculate the 
            #offsets of each line in sequence and return them
            #this generator is used as the linesIterable
            #for the DASHED TrafficLineType
            def linesGenerator():
                for lineIndex in range(numberOfLines):
                    #determine yOffset
                    #this is the height of each previous line
                    #(multiplied by two to account for space between them)
                    #plus the initial offset amount
                    yOffset = (lineIndex * (lineHeight*2)) + initialYOffset
                    #Sidenote: Parens aren't needed here,
                    #but they improve clarity

                    #yield the position and dimensions of the
                    #line including the calculated offset
                    #yield is what makes this a generator rather
                    #than a normal function
                    yield (xOffset, yOffset, lineWidth, lineHeight)

            linesIterable = linesGenerator()

        else:
            #raise a ValueError if the line type is invalid
            #because validateTrafficLineType was already used, this error
            #will only be raised if a line type that exists in the enum but 
            #does not have a corresponding draw function is used.
            errMsg = f"Attempted to draw road with TrafficLineType \"{lineType}\" but found now corresponding draw function!"
            raise ValueError(errMsg)

        #draw each line
        for xOffset, yOffset, lineWidth, lineHeight in linesIterable:

            #draw the line using provided position and dimensions
            if not self.horizontal:
                self.create_rectangle(xOffset, yOffset, xOffset+lineWidth, yOffset+lineHeight, fill=self.LINE_COLOR)
            else:
            #draw lines horizontally if needed
            #this is done by switching around which parameter goes where
                self.create_rectangle(yOffset, xOffset, yOffset+lineHeight, xOffset+lineWidth, fill=self.LINE_COLOR)

        #return True to indicate success
        return True


    #updates the _lineType of this Road to the specified value
    #requires a TrafficLineType or matching string; anything else will produce a ValueError
    #note: this does not redraw the lines; to do this you can call drawRoad manually or simply wait
    #for the _onResize event handler to call drawRoad for you
    def setLineType(self, newLineType: TrafficLineType):
        self._lineType = self.validateTrafficLineType(newLineType)

    #returns the current _lineType of this Road
    def getLineType(self) -> TrafficLineType:
        return TrafficLineType(self._lineType)


    #internal method
    #updates the internal size values
    def _updateSize(self, width = None, height = None):
        self.currentWidth = width if width != None else self.winfo_width()
        self.currentHeight = height if height != None else self.winfo_height()
        self.drawRoad()

    #internal method
    #event handler for <Configure> event which fires when resizing
    def _onResize(self, event):
        if event.width != self.currentWidth or event.height != self.currentHeight:
            self._updateSize(event.width, event.height)


    def __init__(self, parent, horizontal=False):
        from tkinter.constants import FLAT

        #run superclass constructor
        super().__init__(
            parent, #set parent object
            width=100, #set default width and height
            height=100, 
            bg=self.ROAD_COLOR, #set background color
            highlightthickness=0 #remove border that is applied by default to canvas widgets
            )

        #save rotation setting
        self.horizontal = horizontal

        #init line type to the default
        self._lineType = self.DEFAULT_LINE_TYPE

        #get dimensions
        #these will be updated dynamically at runtime
        #using the <Configure> event and onResize method
        self.currentWidth = self.winfo_width()
        self.currentHeight = self.winfo_height()
        
        #bind the _onResize method to the <Configure> event
        self.bind("<Configure>", self._onResize)

        #check for Collisions with other roads
        #store these Collisions in a list, then enable binding on each
        self.roadCollisions: List[Collision] = []
        for roadCollision in self.getRoadCollisions():
            roadCollision.addBindings()
            self.roadCollisions.append(roadCollision)
        #because each of the Collisions is bound, it will update to reflect
        #the new area of collision

        #bind the drawIntersectionBoxes method to the <<CollisionUpdate>> event
        #this will draw intersections over top of existing traffic lines
        self.bind("<<CollisionUpdate>>", self.drawIntersectionBoxes)
        

    #draw a blank rectangle over all areas of this road
    #that intersect another road
    #event parameter is provided so this can be used as an event handler
    def drawIntersectionBoxes(self, event = None):
        for roadCollision in self.roadCollisions:
            #get the corners of the collision area
            try:
                cornerTL, cornerBR = roadCollision.getCollisionCorners()
            except ValueError:
                #ValueError is raised if the collision
                #has no area (i.e. the two objects aren't currently colliding)
                #in that case, continue to the next collision
                continue
            
            #the coordinates returned by the collision are relative
            #to the space in which the collision occured
            #we convert this to the space of this
            #Road by subtracting the Road's coordinates
            thisX, thisY = self.getPos()

            #while converting, unpack corner tuples
            #into 4 seperate variables
            x0 = cornerTL[0] - thisX
            y0 = cornerTL[1] - thisY
            x1 = cornerBR[0] - thisX
            y1 = cornerBR[1] - thisY

            #draw a rectangle using these coordinates
            self.create_rectangle(x0, y0, x1, y1, 
                fill=self.ROAD_COLOR, #fill with the same color as the road
                outline=self.ROAD_COLOR #outline same color as fill
                )    


    #get a list of Collisions for each
    #Road that this Road intersects; these can be used
    #to draw intersections
    def getRoadCollisions(self) -> List[Collision]:

        #define a filter function that will return only 
        #Road objects that are not this one
        roadFilterFunc = lambda x: x != self and isinstance(x, Road)

        #apply that filter function to the list of this Road's parent's children
        #notably this list includes the current Road which is why we include
        #a check for it in the filter function
        siblingRoads = filter(roadFilterFunc, self.master.winfo_children())

        #test collision on these sibling roads and return the results
        roadCollisions = self.getCollisions(siblingRoads)

        return roadCollisions   


#end Road




if __name__ == "__main__":
    print("This is a class definition used as part of a larger script")
    print("Did you mean to run py_traffic_light.py?")
