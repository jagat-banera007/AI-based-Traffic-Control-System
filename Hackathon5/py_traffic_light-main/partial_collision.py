#!/usr/bin/env python3
from __future__ import annotations

from collision import Collision
from typing import TYPE_CHECKING, Tuple

from proportional_bb import ProportionalBB
if TYPE_CHECKING:
    from collider import ColliderInterface


#PartialCollision
#A subclass of Collision that supports setting
#an 'active' area for collision checks
#PartialCollisions will only check for overlapping area
#within the active area of both Colliders
#The active area of each Collider is defined using 
#proportions of its dimensions; see below for details
class PartialCollision(Collision):

    #define the default active area bounds
    DEFAULT_ACTIVE_START = 0.0
    DEFAULT_ACTIVE_END = 1.0
    

    #override constructor
    def __init__(self, collisionSource: ColliderInterface, collidedWith: ColliderInterface):

        #run superclass constructor
        super().__init__(collisionSource, collidedWith)

        #init the active area bound vars
        #each Collider needs a ProportionalBB
        #to store the bounding box of its active area
        self.collisionSourceActiveArea = ProportionalBB(
            self.DEFAULT_ACTIVE_START,
            self.DEFAULT_ACTIVE_END,
            self.DEFAULT_ACTIVE_START,
            self.DEFAULT_ACTIVE_END
            )

        self.collidedWithActiveArea = ProportionalBB(
            self.DEFAULT_ACTIVE_START,
            self.DEFAULT_ACTIVE_END,
            self.DEFAULT_ACTIVE_START,
            self.DEFAULT_ACTIVE_END
            )

    #override collision area calculation
    #to only include active areas for each Collider
    def getCollisionArea(self) -> Tuple[int, int, int, int]:
        #get the ranges that both objects cover
        srcRanges = self.collisionSource.getDimensionRanges()
        objRanges = self.collidedWith.getDimensionRanges()

        #use the ProportionalBB of each Collider to get the
        #active area for collision
        srcActiveRanges = self.collisionSourceActiveArea.calculateDimensionRanges(*srcRanges[0], *srcRanges[1])
        objActiveRanges = self.collidedWithActiveArea.calculateDimensionRanges(*objRanges[0], *objRanges[1])

        #calculate the area of overlap between these ranges
        collisionArea = self.getRectangleOverlap(srcActiveRanges, objActiveRanges)

        #return the result of the collision
        #this will be None if no collision was found
        return collisionArea

  
    #staticmethod
    #Given a Collision, returns a PartialCollision
    #If the provided Collision is already a PartialCollision, return it unchanged
    #If transferBinding is True and the provided Collision
    #is bound, it will be unbound and the returned PartialCollision
    #will be bound instead. If transferBinding is False (default),
    #the provided Collision is unchanged and the new PartialCollision
    #will always be unbound until you manually call its addBindings method
    #Raises TypeError if provided value is not a Collision
    @staticmethod
    def fromCollision(
        targetCollision: Collision, 
        transferBinding: bool = False
        ) -> PartialCollision:

        if isinstance(targetCollision, PartialCollision):
            #if targetCollision is already a PartialCollision,
            #return it without any modification
            return targetCollision
        elif isinstance(targetCollision, Collision):
            #if targetCollision is a Collision but not a
            #PartialCollision, create a new PartialCollision from it
            src = targetCollision.collisionSource
            obj = targetCollision.collidedWith
            newCollision = PartialCollision(src, obj)
            
            #if transferBinding is true, check whether the target collision is bound
            if transferBinding and targetCollision.hasBindings(hasAny=True):
                #If transferBinding is true and the collision is bound,
                #unbind the old collision and then bind the new collision
                targetCollision.removeBindings()
                newCollision.addBindings()

            #return the new PartialCollision
            return newCollision

        else:
            #raise TypeError if targetCollision is not a Collision
            errMsg = f"{targetCollision} is not a Collision!"
            raise TypeError(errMsg) 


if __name__ == "__main__":
    print("This is a class definition used as part of a larger script")
    print("Did you mean to run py_traffic_light.py?")