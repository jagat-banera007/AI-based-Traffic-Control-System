#!/usr/bin/env python3
from __future__ import annotations

from typing import Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from collider import ColliderInterface


#Collision
#Class to represent a collision between two objects
#Includes members to store both collided objects 
#as well as the area of intersection

class Collision():

    #given two ranges as 2-tuples (start, stop)
    #returns one range that is the intersection of the two
    #provided ranges, or None if they do not intersect at all
    @staticmethod
    def getRangeOverlap(rangeA: Tuple[int, int], rangeB: Tuple[int, int]) -> Tuple[int, int]:
        
        #first, ensure that each tuple is ordered
        #properly, with the first value being less or equal
        #to the second value
        if rangeA[0] > rangeA[1]:
            #if tuple is ordered incorrectly,
            #swap positions of the values 
            rangeA = (rangeA[1], rangeA[0])

        #same logic as rangeA
        if rangeB[0] > rangeB[1]:
            rangeB = (rangeB[1], rangeB[0])


        #determine whether any overlap exists.
        #This expression can be read as:
        #if A starts before B ends and B starts before A ends
        if rangeA[0] <= rangeB[1] and rangeB[0] <= rangeA[1]:
            #If overlap exists, determine the overlapping range
            #do this by finding the largest start and smallest end
            overlapStart = rangeA[0] if rangeA[0] > rangeB[0] else rangeB[0]
            overlapEnd = rangeA[1] if rangeA[1] < rangeB[1] else rangeB[1]
            return (overlapStart, overlapEnd)

        else:
            #if no overlap was found, return None
            #this would be done implicitly but I choose to
            #explicitly do it here for clarity's sake
            return None


    #Similar to getRangeOverlap, but takes two sets of 
    #(xRange, yRange) and compares them in two dimensions
    #returns a 4-tuple (x, y, width, height) of the overlapping area
    #or None if there is no overlap
    @classmethod
    def getRectangleOverlap(cls, 
        rectA: Tuple[Tuple[int, int], Tuple[int, int]], 
        rectB: Tuple[Tuple[int, int], Tuple[int, int]]
        ) -> Tuple[int, int, int, int]:

        #check for overlap in x dimension
        xOverlap = cls.getRangeOverlap(rectA[0], rectB[0])
        
        #if there is no overlap in the x dimension, return None
        if xOverlap == None:
            return None

        #check for overlap in y dimension
        yOverlap = cls.getRangeOverlap(rectA[1], rectB[1])

        #return None if no overlap found
        if yOverlap == None:
            return None

        #determine the position of the overlap area
        areaX = xOverlap[0]
        areaY = yOverlap[0]

        #determine dimensions of the overlap area
        areaWidth = xOverlap[1] - xOverlap[0]
        areaHeight = yOverlap[1] - yOverlap[0]

        #return the position and dimensions of the overlap area
        return (areaX, areaY, areaWidth, areaHeight)


    #calculates the collision area between collisionSource and collidedWith
    #returns a 4-tuple (x, y, width, height) of the collision area
    #or None if there is no collision
    def getCollisionArea(self) -> Tuple[int, int, int, int]:
        
        #get the ranges that both objects cover
        srcRanges = self.collisionSource.getDimensionRanges()
        objRanges = self.collidedWith.getDimensionRanges()

        #calculate the area of overlap between these ranges
        collisionArea = self.getRectangleOverlap(srcRanges, objRanges)

        #return the result of the collision
        #this will be None if no collision was found
        return collisionArea


    #called whenever either of the Colliders has a <Configure> event
    #(assuming bindings have been set with Collision.addBindings())
    #raises a <<CollisionUpdate>> event on both Colliders
    def relayCollisionUpdateEvent(self, event = None):

        self.collisionSource.createCollisionUpdateEvent()
        self.collidedWith.createCollisionUpdateEvent()

    #constructor requires two Collider objects; these are the objects involved
    #with this specific Collision instance
    def __init__(self, collisionSource: ColliderInterface, collidedWith: ColliderInterface):

        #init collider storage vars
        self.collisionSource: ColliderInterface = collisionSource
        self.collidedWith: ColliderInterface = collidedWith

        #init vars for funcids (from bindings)
        #these are needed to unbind later
        self._collisionSourceFuncId = None
        self._collidedWithFuncId = None


    #adds <Configure> bindings to both Collider objects
    #that will update the collision area when their size changes
    #if overwrite is set to True (the default), then existing bindings
    #(that were caused by this object) will be overwritten. If overwrite is False,
    #a ValueError is raised when attempting to add bindings if bindings already exist
    def addBindings(self, overwrite = True):
        
        if self._collisionSourceFuncId != None or self._collidedWithFuncId != None:
            if overwrite:
                print(f"Warning: overwriting bindings on {self}")
                self.removeBindings()
            else:
                raise ValueError("Cannot add bindings because bindings already exist!")
                

        self._collisionSourceFuncId = self.collisionSource.bind("<Configure>", self.relayCollisionUpdateEvent, add=True)
        self._collidedWithFuncId = self.collidedWith.bind("<Configure>", self.relayCollisionUpdateEvent, add=True)


    #removes the <Configure> bindings set on Collider objects
    #prints a message and returns False if either binding is already unset
    #returns True if both bindings were set
    def removeBindings(self):
        
        bothWereSet = True

        if self._collisionSourceFuncId != None:
            self.collisionSource.unbind("<Configure>", self._collisionSourceFuncId)
            self._collisionSourceFuncId = None
        else:
            print(f"Warning: Couldn't remove binding on <{self}>.collisionSource because it didn't exist")
            bothWereSet = False

        if self._collidedWithFuncId != None:
            self.collidedWith.unbind("<Configure>", self._collidedWithFuncId)
            self._collidedWithFuncId = None
        else:
            print(f"Warning: Couldn't remove binding on <{self}>.collidedWith because it didn't exist")
            bothWereSet = False

        return bothWereSet

    #methods for use with the python "with" expression
    def __enter__(self):
        return self

    def __exit__(self):        
        self.removeBindings()

    #returns True if there is a collision area, False otherwise
    def hasCollisionArea(self):
        #calculate the collision; if the result isn't None, then
        #there must be a collision area
        return (self.getCollisionArea() != None)


    #returns a 2-tuple (x, y) of the origin coordinates
    #of this collision. Raises a ValueError if there is no collision
    def getCollisionOrigin(self) -> Tuple[int, int]:

        #calculate the collision area
        collisionArea = self.getCollisionArea()

        #if there is a collision area, return its position
        if collisionArea != None:
            origin = (
                collisionArea[0],
                collisionArea[1]
            )
            return origin
        else:
            #if there is no collision area, raise a ValueError
            errMsg = f"Attempted to run <{self}>.getCollisionOrigin but there was no collision area!"
            raise ValueError(errMsg)
        

    #Returns True if this Collision has 
    #active bindings, False if it does not.
    #if hasAny is True (default), returns True if any bindings are active
    #if hasAny is False, only returns True if all bindings are active
    def hasBindings(self, hasAny: bool = True):
        
        if hasAny:
            return (self._collisionSourceFuncId != None or self._collidedWithFuncId != None)
        else:
            return (self._collisionSourceFuncId != None and self._collidedWithFuncId != None)
    
    
    #returns a 2-tuple (width, height) of the
    #dimensions of the collision area. 
    #Raises a ValueError if there is no collision
    def getCollisionDimensions(self) -> Tuple[int, int]:
        
        #calculate the collision area
        collisionArea = self.getCollisionArea()

        #if there is a collision area, return its dimensions
        if collisionArea != None:
            dimensions = (
                collisionArea[2],
                collisionArea[3]
            )
            return dimensions
        else:
            #if there is no collision area, raise a ValueError
            errMsg = f"Attempted to run <{self}>.getCollisionDimensions but there was no collision area!"
            raise ValueError(errMsg)


    #returns a 4-tuple (x, y, width, height) including
    #both the origin coordinates and dimensions of the
    #collision area. This is very similar to the return 
    #value of getCollisionArea; the only difference this function
    #has on that one is that this one will raise a ValueError
    #rather than returning None if there is no collision
    def getCollisionGeometry(self) -> Tuple[int, int, int, int]:
        
        #calculate collision area
        collisionArea = self.getCollisionArea()

        #return if collision area is not none
        if collisionArea != None:
            return collisionArea
        else:
            #raise a ValueError if there is no collision area 
            newMsg = f"Attempted to run <{self}>.getCollisionGeometry but there was no collision area!"
            raise ValueError(newMsg)
            

    #returns a 2-tuple of 2-tuples ((x0,y0), (x1, y1))
    #these are the coordinates of the top left and bottom right
    #corners of the collision area; this could be useful
    #for drawing a rectangle that covers the area
    #raises a ValueError if any of the collision area vars are unset
    def getCollisionCorners(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        
        #calculate collision area
        collisionArea = self.getCollisionArea()

        if collisionArea != None:
            #if collision area is not None, calculate corners
            #and return as a tuple of tuples
            x, y, width, height = collisionArea
            cornerTL = (x, y)
            cornerBR = (x + width, y + height)
            return (cornerTL, cornerBR)
        else:
            #if collision area is None, raise a ValueError
            newMsg = f"Attempted to run <{self}>.getCollisionCorners but there was no collision area!"
            raise ValueError(newMsg)

    def __repr__(self):
        return f'Collision({repr(self.collisionSource)}, {repr(self.collidedWith)})'

    #override __str__ to describe collision
    def __str__(self):
        fStr = repr(self)
        collisionArea = self.getCollisionArea()
        if collisionArea == None:
            fStr += f"; (No Collision)"
        else:
            fStr += f'; (x: {collisionArea[0]}, y:{collisionArea[1]}, width:{collisionArea[2]}, height: {collisionArea[3]})'
        return fStr
