#!/usr/bin/env python3
from __future__ import annotations

from typing import ClassVar, Tuple, Dict, Any
from dataclasses import dataclass

#ProportionalBB (Short for Proportional Bounding Box)
#A data class used to store a bounding box that is defined
#as proportions of some rectangle.
#Each dimension is defined by a start and end bound,
#with each of those being a floating point number from 0.0 to 1.0
#note: a dataclass is not a great fit for this purpose
#if this were production code, I would write a class from scratch instead
#this design was chosen mostly because I wanted to experiement
@dataclass
class ProportionalBB:
    
    #dictionary that associates the x and y axes
    #with a tuple of bound names (start, end)
    AXIS_BOUNDS : ClassVar[Dict[str, Tuple[str, str]]] = {
        "x": ("xStart", "xEnd"),
        "y": ("yStart", "yEnd")
        }

    #define the instance vars for bounds
    xStart: float
    xEnd: float
    yStart: float
    yEnd: float

    #define the 'silent' instance var with
    #a default value of False
    silent: bool = False

    ### NOTES ON PROPORTIONAL AREA DEFINITION ###
    # A proportional area is defined by four bounds in total:
    # - the X dimension start bound
    # - the X dimension end bound
    # - the Y dimension start bound
    # - the Y dimension end bound
    # this allows you to define a rectangle
    # relative to some other rectangle
    #
    # bounds are defined as the portion 
    # of the total dimension (x or y) that lays behind the boundary
    # for example:
    #  a bound at 0.0 is at the start
    #  a bound at 0.5 is in the middle
    #  a bound at 1.0 is at the end
    # bounds are defined in this way so that if the size of
    # a rectangle changes, the  bounds stay in the same positions
    # relative to each other and the borders of the widget (though
    # this necessarily changes the actual pixel position of the bound)
    ########################################

    #internal method
    #ensure that bound is within the range 0 to 1 inclusive
    #return the value as a float
    #raise a ValueError if bound is outside the range 0 to 1 inclusive
    #raise a TypeError if bound isn't and can't be converted to a float
    @staticmethod
    def _validateBoundValue(bound: float, silent: bool = False):
        try:
            #check type of bound
            if not isinstance(bound, float):
                #attempt conversion if not a float
                #after printing a warning message
                if not silent:
                    print(f"Warning: casting {bound} to float")
                bound = float(bound)
        except (TypeError, ValueError):
            #A ValueError may be thrown if a string is passed
            #that can't be converted to a float
            #A TypeError may be thrown if another type of object is passed
            #In both cases, raise a TypeError with a custom message
            errMsg = f"Bound value is not a float and could not be converted ({repr(bound)})"
            raise TypeError(errMsg)

        #ensure bound is not outside the 0 to 1 range
        if bound < 0 or bound > 1:
            #if an erroring bound was detected, raise a ValueError
            errMsg =  f"Bound is out of range ({repr(bound)})"
            raise ValueError(errMsg)

        return bound

    #returns a list of all configured bound names
    #as provided by AXIS_BOUNDS
    @classmethod
    def getBoundNames(cls):
        boundNames = []
        boundNameSets = cls.AXIS_BOUNDS.values()
        for nameSet in boundNameSets:
            boundNames += nameSet
        return boundNames

    #override __setattr__ (called when any attribute is set)
    #to run the bound validation method on the prospective
    #new bound before actually setting it
    #see definition of validateBound for details on raised exceptions
    def __setattr__(self, name: str, value: Any) -> None:
        
        #if the attribute is not a bound, use the normal
        #__setattr__ method instead of this custom one
        if name not in self.getBoundNames():
            #print("name not found:", name)
            #print("current names:", self.__dict__.keys())
            return super().__setattr__(name, value)
        
        else:
            #ensure the value is of valid type and not outside the 0 to 1 range
            value = self._validateBoundValue(value, silent = self.silent)

            #determine whether this is the start or end bound
            #and which axis it is on
            isStart = None
            selectedAxis = None
            for axisName, boundNames in self.AXIS_BOUNDS.items():
                
                #check the selected name against both bound names
                #if it matches, set isStart appropriately
                if name == boundNames[0]:
                    isStart = True
                elif name == boundNames[1]:
                    isStart = False

                #if the name was matched, capture 
                #the axis name and stop iterating
                if isStart != None:
                    selectedAxis = axisName
                    break

            
            try:
                #get the value of the opposite bound
                if isStart:
                    oppositeValue = getattr(self, self.AXIS_BOUNDS[selectedAxis][1])
                else:
                    oppositeValue = getattr(self, self.AXIS_BOUNDS[selectedAxis][0])

            except AttributeError:
                #AttributeError may be raised if 
                #the opposite value does not yet exist
                #in this case, accept the value immedately
                return super().__setattr__(name, value)

            #if the opposite bound is set, 
            #check the new value against it
            if isStart:
                #if the bound is the start,
                #raise a ValueError if the 
                #new value is not less than
                #the end bound value
                if value >= oppositeValue:
                    return super().__setattr__(name, value)
                else:
                    errMsg = f"New value for top bound ({value}) must be less than bottom bound ({oppositeValue})"
                    raise ValueError(errMsg)
            
            else:
                #if the bound is the end,
                #raise a ValueError if the 
                #end bound value is not 
                #less than the new value
                if oppositeValue <= value:
                    return super().__setattr__(name, value)
                else:
                    errMsg = f"New value for bottom bound ({value}) must be greater than than top bound ({oppositeValue})"
                    raise ValueError(errMsg)

    #end __setattr__        

    #Given a range (in the form of two numeric values rangeStart and rangeEnd),
    #calculates the actual numeric range of this ProportionalBB over that range
    #on the specified axis. The axis is controlled by isX: 
    # if true (default), the X bounds are used; if false, the y bounds are used
    #Raises a ValueError if provided end is not greater than provided start
    #For example:
    #
    # A range of 0, 100 
    # on a Proportional axis with bounds 0.0, 1.0 
    # returns (0, 100)
    #
    # A range of 100, 500 
    # on a Proportional axis with bounds 0.0, 1.0 
    # returns (100, 500)
    #
    # A range of 0, 100 
    # on a Proportional axis with bounds 0.25, 0.75 
    # returns (25, 75)
    #
    # A range of 100, 500 
    # on a Proportional axis with bounds 0.25, 0.75 
    # returns (200, 400)
    def calculateRange(self,
        rangeStart: int or float, 
        rangeEnd: int or float, 
        isX: bool = True
        ) -> Tuple[float, float]:
        
        #get the overall size of the range
        rangeSize = rangeEnd - rangeStart

        #raise a ValueError if rangeSize is invalid
        if rangeSize <= 0:
            errMsg = f"Provided rangeEnd ({rangeEnd}) was not greater than provided rangeStart ({rangeStart})"
            raise ValueError(errMsg)

        #get the proportional bound values for the specified axis
        if isX:
            startBoundProportion = self.xStart
            endBoundProportion = self.xEnd
        else:
            startBoundProportion = self.yStart
            endBoundProportion = self.yEnd

        #calculate the literal bound values using the proportional ones
        #each literal bound value is a proportion of the overall 
        #range size offset by the start position of the range 
        startBound = (startBoundProportion * rangeSize) + rangeStart
        endBound = (endBoundProportion * rangeSize) + rangeStart

        return (startBound, endBound)

    #Given two sets of ranges (one for both x and y axes),
    #uses self.calculateRange on both and returns the result
    #as a 2-tuple of 2-tuples ((xStart, xEnd), (yStart, yEnd))
    #Raises a ValueError if either range has an end that
    #is not greater than that range's start
    def calculateDimensionRanges(self, 
        xStart: int or float,
        xEnd: int or float,
        yStart: int or float,
        yEnd: int or float
        ) -> Tuple[Tuple[float, float], Tuple[float, float]]:

        #calculate x axis
        xRange = self.calculateRange(xStart, xEnd, True)
        #calculate y axis
        yRange = self.calculateRange(yStart, yEnd, False)
        
        return (xRange, yRange)


    #staticmethod
    #given a desired value within a range defined by
    #rangeStart and rangeEnd, returns the proportion of that range
    #That is, translates a pixel index within a range to a proportion of that range
    #that the desired value is - so if you have x0 and x1 (or y0 and y1)
    #for an object as well as a desired pixel position between those points,
    #you can use this function to find what to set one of a ProportionalBB's
    #bounds such that the bound lies exactly at the desired position
    #always returns a float between 0 and 1
    #raises a ValueError if range is invalid or desired value not within it
    @staticmethod
    def calculateProportion(
        rangeStart: int or float,
        rangeEnd: int or float,
        desiredValue: int or float
        ) -> float:
        
        #raise ValueError if range is not greater than zero
        if rangeEnd < rangeStart:
            errMsg = f"Range end ({rangeEnd}) was not greater than rangeStart ({rangeStart})"
            raise ValueError(errMsg)

        #raise ValueError if desired value is not in range
        if desiredValue < rangeStart or desiredValue > rangeEnd:
            errMsg = f"Value {desiredValue} not found in range {rangeStart} to {rangeEnd}"
            raise ValueError(errMsg)

        #calculate the desired value as a proportion of 
        #the overall range size
        rangeSize = rangeEnd - rangeStart
        return (desiredValue - rangeStart) / rangeSize


    #returns a shallow copy of this object
    def getCopy(self) -> ProportionalBB:
        from dataclasses import replace
        return replace(self)

if __name__ == "__main__":
    print("This is a class definition used as part of a larger script")
    print("Did you mean to run py_traffic_light.py?")
  