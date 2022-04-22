#!/usr/bin/env python3

from tkinter import Frame

#The primary frame for the application
class PrimaryFrame(Frame):

    #default minimum width and height of the Primary Frame
    FRAME_SIZE = 600

    #define the names of the traffic lights
    #as well as their ordering when selecting them
    #sequentially
    TLIGHT_NAMES = (
        "north",
        "east",
        "south",
        "west"
        )

    #define the coordinates of each traffic light
    #as 2-tuples (row, column)
    TLIGHT_COORDINATES = {
        "north" : (1, 2),
        "south" : (3, 2),
        "east"  : (2, 3),
        "west"  : (2, 1)
        }


    #some of the initialization includes making changes to the parent
    #including setting a grid layout and setting the minimum row and column size
    #these changes are all included here, so that they can be easily skipped if desired
    def _makeChangesToParent(self):

        #configure row and column minimum size in parent window
        self.master.rowconfigure(index=0, weight=1, minsize=self.FRAME_SIZE)
        self.master.columnconfigure(index=0, weight=1, minsize=self.FRAME_SIZE)

        #set minimum size of window
        self.master.minsize(width=self.FRAME_SIZE, height=self.FRAME_SIZE)

        #put frame into parent window
        self.grid(row=0, column=0, padx=25, pady=25, sticky="NESW")
        

    #internal method used to
    #set up attributes for PrimaryFrame
    def _setFrameAttributes(self):
        

        #set border attributes
        self.configure(borderwidth=2, relief="solid")

        #set background color
        self.configure(background="#FFFFFF")
        
        #setup grid structure
        for x in range(5):
            self.rowconfigure(index=x, weight=1, minsize=100)
            self.columnconfigure(index=x, weight=1, minsize=100)

    #internal method used to
    #set up the widgets on the page
    #including traffic lights and roads
    def _placeWidgets(self):
        from road import Road
        from traffic_light import TrafficLight
        from vehicle import Vehicle

        #create and position road widgets
        self.vertRoad = Road(self)
        self.vertRoad.grid(row=0, column=2, sticky="NS", rowspan=5)

        self.horizRoad = Road(self, True)
        self.horizRoad.grid(row=2, column=0, sticky="EW", columnspan=5)

        #place vehicle
        self.vehicle = Vehicle(self)
        self.vehicle.place(x=0, y=0)

        #create and position each light
        for tlightName in self.TLIGHT_NAMES:
            
            #create the light
            trafficLight = TrafficLight(self)

            #get the traffic light's coordinates 
            rowCoord, colCoord = self.TLIGHT_COORDINATES[tlightName]
            
            #place the traffic light within this frame
            trafficLight.grid(row=rowCoord, column=colCoord)

            #save the light by name in the self.trafficLights dictionary
            #this allows it to be accessed later
            self.trafficLights[tlightName] = trafficLight
        
       
        
            

    #init requires parent window as first parameter
    #noGridChange controls whether the parent window's row/column configs
    #will be affected; if true, they are left alone
    def __init__(self, parentWindow, noGridChange = False):
        from typing import Dict
        from road import Road
        from traffic_light import TrafficLight
        from vehicle import Vehicle

        #run superclass constructor
        super().__init__(
            parentWindow, 
            width=self.FRAME_SIZE, 
            height=self.FRAME_SIZE
            )
        
        
        #setup frame attributes
        self._setFrameAttributes()

        #do initialization requiring changes to parent window
        #unless noGridChange is set to True
        if not noGridChange:
            self._makeChangesToParent()

        #create vars for storing roads
        #roads are created within _placeWidgets
        self.horizRoad : Road = None
        self.vertRoad : Road = None

        #create var for storing vehicle
        #vehicle is created within _placeWidgets
        self.vehicle : Vehicle = None

        #init traffic lights dictionary (with type hint)
        self.trafficLights : Dict[str, TrafficLight] = {}
        
        #instantiate and position widgets (roads, traffic lights; etc)
        self._placeWidgets()

        #initialize selected light name with the first 
        #this can be used to interact with the lights sequentially
        #using the getSelectedLight and incrementSelectedLight methods
        self.selectedLightName = self.TLIGHT_NAMES[0]


    #returns the currently selected light name
    def getSelectedLightName(self):
        return self.selectedLightName

    #increments the currently selected light name
    def incrementSelectedLightName(self):
        #get the index of the currently selected light naame
        selectedLightIndex = self.TLIGHT_NAMES.index(self.selectedLightName)

        #get the index of the next light by adding 1
        nextIndex = selectedLightIndex + 1

        #if the selected light name is not the last one in the list,
        #set the new selected light name to the next name in the list
        if nextIndex < len(self.TLIGHT_NAMES):
            self.selectedLightName = self.TLIGHT_NAMES[nextIndex]

        #if the selected light name is the last one in the list,
        #set the new selected light name to the first one in the list
        else:
            self.selectedLightName = self.TLIGHT_NAMES[0]

    
    #similar to getSelectedLightName but returns the actual
    #TrafficLight instance instead
    def getSelectedLight(self):
        from traffic_light import TrafficLight
        selectedName = self.getSelectedLightName()
        selectedLight : TrafficLight = self.trafficLights[selectedName]
        return selectedLight

    #alias for incrementSelectedLightName
    #to better match the form of getSelectedLight
    def incrementSelectedLight(self):
        self.incrementSelectedLightName()
            

    

#end PrimaryFrame

if __name__ == "__main__":
    print("This is a class definition used as part of a larger script")
    print("Did you mean to run py_traffic_light.py?")