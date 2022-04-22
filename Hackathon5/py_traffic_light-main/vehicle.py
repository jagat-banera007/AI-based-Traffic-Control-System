#!/usr/bin/env python3

from tkinter import Canvas
from collider import Collider


#a widget to represent a vehicle; can "drive"
#across a Frame

class Vehicle(Collider, Canvas):

    DEFAULT_COLOR = "#FF0000"

    DEFAULT_WIDTH = 50
    DEFAULT_HEIGHT = 50

    #The default delay between frames of movement
    #as an integer number of milliseconds
    DEFAULT_MOVEMENT_DELAY = 16

    #The default distance covered per frame
    #as an integer number of pixels
    DEFAULT_MOVEMENT_DISTANCE = 1

    #override constructor
    def __init__(self, parent, movementDelay: int = None, movementDistance: int = None):
        #set defaults in superclass constructor
        super().__init__(
            parent,
            width=self.DEFAULT_WIDTH,
            height=self.DEFAULT_HEIGHT,
            bg=self.DEFAULT_COLOR
            )

        #init animation control variables
        self.movementDelay = movementDelay 
        self.movementDistance = movementDistance
        self.lastFrameTime = None

        #set defaults if no value was provided for either control var
        if movementDelay == None:
             self.movementDelay = self.DEFAULT_MOVEMENT_DELAY
        if movementDistance == None:
             self.movementDistance = self.DEFAULT_MOVEMENT_DISTANCE

        #init _destination to None
        #this will be set to a 2-tuple (x, y)
        #when animating movement from point to point
        #being set to None indicates no active movement
        self._destination = None

    #draws vehicle
    def drawVehicle(self):
        self.create_rectangle(0,0, self.winfo_width(), self.winfo_height())


    #given x and y coordinates (within this 
    #vehicle's parent), updates the vehicle's position
    #visually, the vehicle will appear to snap to the specified coordinates
    def setPos(self, xPos: int, yPos: int):
        self.place(x=xPos, y=yPos)

    
    #move to specified destination in an animated way
    #note that this method DOES NOT BLOCK!!!
    #execution will return from this method 
    #long before the vehicle reaches its destination
    #if you need to do something after the drive completes, 
    #bind a method to the <<DriveComplete>> method of this Vehicle
    #when the drive completes 
    def driveToPos(self, xPos: int, yPos: int):

        # The way that movement animation works internally
        # is not entirely clear, so I will explain it here.
        # The basic principle is this: instead of jumping directly
        # to the destination, take multiple small steps towards the destination
        # and introduce some time delay between each step.
        # In a perfect world this delay could come from time.sleep,
        # but this would also stop execution of other GUI related code and
        # therefore can't be used in this case; tkinter's after method 
        # must be used instead

        # The after method executes a function after a delay; this means
        # that each movement step must be a discrete function call. For Vehicles,
        # the _animStep method is used. _animStep requires that _destination be set;
        # if it isn't then no movement will be performed - why the destination needs to be 
        # a class variable is left as an excersize to the reader 
        # (hint: discrete function calls means discrete scopes)

        # To actually start animation, this method only needs to set the
        # _destination variable and call the _animStep method the first time;
        # _animStep will call itself as many times as it needs to
        # until the destination is reached

        # Before doing this however, the method checks if a drive is already
        # active. If there is an active drive, a ValueError is raised as two
        # drive operations can't take place simultaniously
        if self.isDriving():
            raise ValueError("Cannot start driving when a drive operation is already active")
        else:
            self._destination = (xPos, yPos)
            self._animStep()

    #internal method to make one step of movement towards current destination
    #calls itself after a delay to continue moving, if needed
    #returns immediately if no destination is set, or if destination is already reached
    def _animStep(self):
        from datetime import datetime

        #check for missing destination        
        if self._destination == None:
            print("anim step missing destination")
            #if destination is missing, return now
            return
        #if destination isn't missing, break it out into x and y
        else:
            destX, destY = self._destination

        #get current position
        currentX, currentY = self.getPos()
        
    
        #if current position exactly matches destination,
        #clear destination, raise a <<DriveComplete>> event,
        #then return without moving the vehicle
        if destX == currentX and destY == currentY:
            self.event_generate("<<DriveComplete>>", when="tail")
            self.abortDrive()
            return

        #to guarantee correct speed, the deviation of the
        #actual delay time from the desired delay time
        #must be matched with an equivalent deviation in distance
        #to calculate this distance deviation, we first calculate
        #the time deviation of the last frame

        #measure current time against last frame time to find
        #the actual time between frames in milliseconds
        currentTime = datetime.now()
        try:
            actualDelay = (currentTime - self.lastFrameTime).total_seconds() * 1000
        except TypeError:
            #TypeError is raised if lastFrameTime isn't set
            #in this case, set actual to the movement delay
            actualDelay = self.movementDelay
        
        #adjusted distance is the same proportion of 
        #movement distance that actual delay is of movement delay
        adjustedDistance = int(self.movementDistance * (actualDelay/self.movementDelay))

        #determine new X position based on current position,
        #destination position, and adjusted movement distance
        if destX > currentX:
            #the min expression ensures that the destination is never overshot,
            #as the adjustedDistance is selected if and only if
            #it is less than the remaining distance to the destination
            newX = currentX + min(destX - currentX, adjustedDistance)
        elif destX < currentX:
            newX = currentX - min(currentX - destX, adjustedDistance)
        else:
            #if destination X exactly equals current X, then newX
            #is set to current X, resulting in no X movement
            newX = currentX

        #determine new Y position using similar logic to X position
        if destY > currentY:
            newY = currentY + min(destY - currentY, adjustedDistance)
        elif destY < currentY:
            newY = currentY - min(currentY  - destY, adjustedDistance)
        else:
            newY = currentY

        #set the new position
        self.setPos(newX, newY)

        #repeat process after delay
        self.after(self.movementDelay, self._animStep)
        
        #after all processing for this animation step,
        #set the lastFrameTime so the frameDelta 
        #(deviation from expected delay) can be calculated
        self.lastFrameTime = datetime.now()


    #drive in a specified cardinal direction
    #by a specified distance (in pixels)
    #valid directions are the strings:
    #"up", "down", "left", and "right"
    #similar to driveToPos, this method DOES NOT BLOCK
    def driveDistance(self, distance: int, direction: str):

        #round distance to the nearest integer that is
        #greater than zero
        distance = int(round(distance))

        #get current position
        x, y = self.getPos()

        #either add or subtract 'distance' to one of the axes
        #depending on the specified direction
        if direction == "up":
            y -= distance
        elif direction == "down":
            y += distance
        elif direction == "left":
            x -= distance
        elif direction == "right":
            x += distance
        else:
            #if direction is not one of the above four strings,
            #raise a ValueError
            raise ValueError(f"Invalid direction: {direction}")

        #drive to the calculated coordinates
        self.driveToPos(x, y)

    #methods for driving in cardinal directions by a distance
    #all four call driveDistance internally and will behave similarly
    def driveUp(self, distance: int):
        self.driveDistance(distance, "up")

    def driveDown(self, distance: int):
        self.driveDistance(distance, "down")

    def driveLeft(self, distance: int):
        self.driveDistance(distance, "left")

    def driveRight(self, distance: int):
        self.driveDistance(distance, "right")

    #returns True if a movement is currently active; False otherwise
    def isDriving(self):
        return self._destination != None

    #stop animated movement, if one is currently active
    def abortDrive(self):
        self._destination = None
        self.lastFrameTime = None


    #returns current speed setting of
    #this vehicle in pixels per second
    #the set of possible speeds is a subset of 
    #the rational numbers (integers divided by integers)
    #but does not include all of them
    def getSpeed(self) -> float:

        #the speed of a vehicle is not stored directly;
        #speed is a measure of distance over time and therefore can
        #be calculated based on movementDistance and movementDelay

        #get a number of pixels per millisecond by dividing
        #the number of pixels traveled in one step by the duration of that step
        pixelsPerMs = self.movementDistance / self.movementDelay

        #convert pixels per millisecond to pixels per second
        #by multiplying by the number of milliseconds in one second (1000)
        pixelsPerSec = pixelsPerMs * 1000

        return pixelsPerSec

    #given a number of pixels per second, adjusts the
    #movement speed and movement distance to make the 
    #Vehicle "drive" at approximately the desired speed
    #note: the actual speed set will be a rational number
    #approximtion of the desired speed, but not nessecarily 
    #the best rational approximation - speeds with
    #denominators (movement delays) closer to the default are preferred
    #returns the actual speed that was set,  
    #same as the result of the getSpeed method
    def setSpeed(self, desiredPixelsPerSecond: float) -> float:

        #convert pixels per second to pixels per millisecond,
        #as the time unit used for delay is milliseconds
        desiredSpeed = desiredPixelsPerSecond / 1000

        #calculate the movement distance required to achieve
        #the desired speed with the default movement delay
        idealMovementDistance = desiredSpeed * self.DEFAULT_MOVEMENT_DELAY

        #the ideal movement distance may be (probably is) fractional
        #but the actual movement distance must be an integer greater than 
        #or equal to 1. we can approach the desired speed by 
        #using the closest approximation of the ideal distance 
        #in combination with an adjusted movement delay

        #set the movement distance to the closet integer approximation
        #of the ideal distance that is 1 or greater
        self.movementDistance = max(1, int(round(idealMovementDistance)))

        #given that movement distance and the desired speed, find
        #the ideal movement delay. since only the actual delay is
        #needed, this ideal delay is immediately rounded to the nearest
        #integer that is greater or equal to 1
        self.movementDelay = max(1, int(round(self.movementDistance / desiredSpeed)))

        #calculate the actual speed based on the set
        #distance and delay and return the result
        return self.getSpeed()
