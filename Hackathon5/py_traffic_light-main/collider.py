#!/usr/bin/env python3
from __future__ import annotations

from position_reporter import PositionReporterInterface, PositionReporter
from typing import Iterable, List, Tuple
from collision import Collision

#Collider Interface
#A subinterface of PositionReporter that can
#detect collisions between itself and other objects
#that implement the Collider Interface
#Descriptions of the expected behavior of each method can be found
#in the concrete PositionReporter definition
class ColliderInterface(PositionReporterInterface):

    _ERROR_MESSAGE_TEXT = "ColliderInterface is abstract and does not provide concrete method definitions"

    def getCollisionWith(self, otherObj: ColliderInterface) -> Collision:
        raise NotImplementedError(ColliderInterface._ERROR_MESSAGE_TEXT)

    def getDimensionRanges(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        raise NotImplementedError(ColliderInterface._ERROR_MESSAGE_TEXT)

    def getCollisions(self, objectsToCheck: Iterable[ColliderInterface] = None) -> List[Collision]:
        raise NotImplementedError(ColliderInterface._ERROR_MESSAGE_TEXT)

    def getCollidingObjects(self, objectsToCheck: Iterable[ColliderInterface] = None) -> List[ColliderInterface]:
        raise NotImplementedError(ColliderInterface._ERROR_MESSAGE_TEXT)

    def generateCollisions(self, colliders: Iterable[ColliderInterface]) -> List[Collision]:
        raise NotImplementedError(ColliderInterface._ERROR_MESSAGE_TEXT)

    def createCollisionUpdateEvent(self) -> None:
        raise NotImplementedError(ColliderInterface._ERROR_MESSAGE_TEXT)

#Collider
#a sub"concrete interface" of PositionReporter that can detect 
#collisions between itself and other Collider instances

class Collider(ColliderInterface, PositionReporter):

    #creates a new Collision object involving this Collider
    #and another provided Collider object
    #raises TypeError if the other object is not a Collider 
    def getCollisionWith(self, otherObj: ColliderInterface) -> Collision:
        if isinstance(otherObj, ColliderInterface):
            return Collision(self, otherObj)
        else:
            raise TypeError(f"{otherObj} does not implement ColliderInterface")


    #returns two ranges as 2-tuples (start, stop)
    #the first range is the x range of the object, the second is the y range
    #these ranges encompass all points along each axis that are
    #within the bounds of the object
    def getDimensionRanges(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        cornerTL, cornerBR = self.getCorners()
        xRange = (cornerTL[0], cornerBR[0])
        yRange = (cornerTL[1], cornerBR[1])
        return (xRange, yRange)


    #returns a list of Collision objects; 
    #one for each object this collider overlaps with
    #if you just want a list of widgets this object 
    #collides with, use getCollidingObjects instead
    #checks against objectsToCheck if provided
    #checks against this object's direct siblings if objectsToCheck is left empty
    #   note: Collisions can raise a <<CollisionUpdate>> event on its Colliders
    #   but you will need to call the addBindings method to activate this
    #   The generateCollisions method may be a better option if
    #   you want all Collisions to have active bindings from the start
    def getCollisions(self, objectsToCheck: Iterable[ColliderInterface] = None) -> List[Collision]:

        #if no object list was provided, use siblings of this object
        if objectsToCheck == None:
            objectsToCheck = self.master.winfo_children()

        #init list of found collisions
        foundCollisions = []
        
        #iterate through objectsToCheck
        #filter is used to filter out this 
        #object from the list, if present
        for obj in filter(lambda x: x != self, objectsToCheck):

            #if object doesn't implement ColliderInterface, then skip 
            #collision check and continue to the next object
            if not isinstance(obj, ColliderInterface):
                continue
            #note: given that PositionReporter has static methods
            #that should work for any rectangular object, only checking against
            #other Colliders isn't strictly necessary. It is done here for performance;
            #to skip checking collision with objects that we aren't 
            #interested in collisions with (such as the background)

            #create a Collision object for these two Colliders
            newCollision = self.getCollisionWith(obj)

            #if objects don't overlap, continue to next object
            if not newCollision.hasCollisionArea():
                continue
            else:
                #if objects do overlap, record this collision
                foundCollisions.append(newCollision)
        
        #after iterating through all objects, return the
        #set of found collisions
        return foundCollisions


    #similar to getCollisions, but only returns
    #the widgets that this object collides with; 
    #no data on the position or size of the collision is included.
    #objectsToCheck works the same as in getCollisions
    def getCollidingObjects(self, objectsToCheck: Iterable[ColliderInterface] = None) -> List[ColliderInterface]:
        
        #get collisions along with unneeded data
        collisions = self.getCollisions(objectsToCheck)

        #strip unneeded data using map
        #list is used to evaluate the result of map into a list
        #if this wasn't done, the function would return an iterator
        #instead of a list, which could lead to unusual problems
        #Unfortunately, doing this mostly negates the performance benefit of using map
        #but this lost performance is probably worth it in this case
        return list(map(lambda x: x.collidedWith, collisions))

    
    #Given an iterable containing Colliders, generates one 
    #Collision object for each Collider. This is unlike getCollisions
    #in that it does not check whether the collision is currently active
    #or not, and that the Collisions returned by this method have already had 
    #their addBindings method called so they can update their sizes
    def generateCollisions(self, colliders: Iterable[ColliderInterface]) -> List[Collision]:

        collisions = []
        for obj in colliders:
            newCollision = self.getCollisionWith(obj)
            newCollision.addBindings()
            collisions.append(newCollision)

        return collisions

    #raises a custom type of event on this Collider
    #this is called by bound Collisions that 
    #this Collider is involved in when the overlapping area changes
    def createCollisionUpdateEvent(self):
        self.event_generate("<<CollisionUpdate>>", when="tail")

#end Collider
        