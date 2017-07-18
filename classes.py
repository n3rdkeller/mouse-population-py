"""A little simulation of a population

This program shows you how classes work.
There were some Classes given: World, Thing, Plant, Corn, Creature, Mouse

Mouse and Corn can multiply and Mouse can also eat corn, but a Mouse can also
die of starvation, if it does not eat the Corn in the right amount of cycles.

Let´s Try
"""

import random
from time import sleep
import os
import sys

class World:
    def __init__(self, mapWidth = 79, mapHeight = 24):
        '''Initializes the world map'''
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.worldMap = [[None for y in range(self.mapHeight)] for x in range(self.mapWidth)]
        self.objects = {}
        random.seed()

    def addObj(self, thing, x, y):
        '''Adds the given Thing to the given position in the world'''
        self.worldMap[x][y] = thing
        self.objects.update({(x, y): thing})
        thing.pos = (x, y)

    def getRandomCoords(self):
        return random.randint(0, self.mapWidth - 1), random.randint(0, self.mapHeight - 1)

    def spawn(self, count, typ):
        '''Spawns count of typ on the map'''
        theType = eval(typ)
        for i in range(count):
            x, y = self.getRandomCoords()
            counter = self.mapWidth * self.mapHeight
            while (self.getObj(x, y) is not None) and (counter is not 0):
                x, y = self.getRandomCoords()
                counter -= 1
            if self.getObj(x, y) is None:
                self.addObj(theType(self), x, y)
        self.clearScreen()

    def delObjByPos(self, x, y):
        '''Removes the Thing from the given position'''
        self.worldMap[x][y] = None
        for coords, thing in self.objects.items():
            if coords == (x, y):
                del self.objects[coords]
                break

    def delObj(self, thing):
        '''Removes the given thing from the object dictionary'''
        self.delObjByPos(thing.pos[0], thing.pos[1])

    def computeLifeCycle(self, count):
        '''Iterates randomly over all things and performs their actions'''
        for i in range(count):
            objects = list(self.objects.values())
            random.shuffle(objects)
            for obj in objects:
                obj.performAction()
            self.clearScreen()
            self.printMap()
            sleep(0.1)
            self.clearScreen()

    def clearScreen(self):
        '''Clears the terminal window'''
        if os.name == "posix": # Linux, Unix etc.
            os.system("clear")
        elif sys.stdin.encoding.lower() == "cp1252": # IDLE
            print(1000 * "\n")
        elif os.name in ("nt", "dos", "ce"): # Windows
            os.system("cls")
        else:
            print(80 * "\n")

    def printMap(self):
        '''Prints the world map with the symbols from the class definition'''
        mapStr = ""
        for y in range(0, len(self.worldMap[0])):
            for x in range(0, len(self.worldMap)):
                mapStr += self.getObjString(x, y)
            mapStr += "\n"
        print(mapStr)

    def getPos(self, thing):
        '''Returns the position of a given Thing as x, y'''
        for coords, obj in self.objects:
            if obj == thing:
                return coords
        # if thing is not found, return None
        return None

    def getObj(self, x, y):
        '''Returns the object at a given position'''
        return self.worldMap[x][y]

    def addNeighbor(self, thing):
        directions = [0, 1, 2, 3]
        direction = random.choice(directions)
        x, y = self.getNeighborCoords(thing.pos[0], thing.pos[1], direction)
        while (self.getObj(x, y) is not None):
            directions.remove(direction)
            if len(directions) == 0:
                return
            direction = random.choice(directions)
            x, y = self.getNeighborCoords(thing.pos[0], thing.pos[1], direction)
        self.addObj(type(thing)(self), x, y)

    def getNeighbor(self, x, y, direction):
        '''Returns the neighbor obj in the given direction'''
        nx, ny = self.getNeighborCoords(x, y, direction)
        return self.getObj(nx, ny)

    def getNeighborCoords(self, x, y, direction):
        '''Returns the neighbor coordinates in the given direction
        North = 0
        South = 1
        West = 2
        East = 3'''
        if direction == 0:
            return x, (y - 1) % self.mapHeight
        elif direction == 1:
            return x, (y + 1) % self.mapHeight
        elif direction == 2:
            return (x - 1) % self.mapWidth, y
        elif direction == 3:
            return (x + 1) % self.mapWidth, y
        else:
            return 255,255

    def getObjString(self, x, y) -> str:
        '''Returns the string of the object at a given position'''
        o = self.getObj(x, y)
        return self.objString(o)

    def objString(self, obj):
        t = type(obj)
        if obj is None:
            return "."
        else:
            return obj.symbol

    def move(self, thing, direction):
        '''Moves a given thing to a given position'''
        oldX, oldY = thing.pos[0], thing.pos[1]
        newX, newY = self.getNeighborCoords(oldX, oldY, direction)
        # delete old object from dict and worldmap
        self.delObjByPos(oldX, oldY)
        # change thing to new Coordinates
        self.addObj(thing, newX, newY)
        thing.changePos(newX, newY)

class Thing(World):
    symbol = "T"
    age = 0
    pos = [None, None]
    world = None

    def __init__(self, world):
        self.world = world

    def performAction(self):
        '''Performs the action of the thing, e.g. increase age'''
        self.age += 1

    def changePos(self, newX, newY):
        pos = [newX, newY]

class Plant(Thing):
    '''Represents a Plant which is a thing'''
    symbol = "P"
    world = None

    def __init__(self, world):
        self.world = world

class Corn(Plant):
    '''This class represents a Corn plant which is a Plant'''
    symbol = "§"
    seedCycle = 6
    currentCycle = 0

    def performAction(self):
        self.currentCycle += 1
        if self.currentCycle % self.seedCycle == 0 and self.currentCycle != 0:
            self.world.addNeighbor(self)

class Creature(Thing):
    '''This class represents a Creature which is a Thing'''
    symbol = "C"
    world = None

    def __init__(self, world):
        self.world = world

class Mouse(Creature):
    '''This class represents a Mouse, which is a Creature'''
    symbol = "M"
    offspringCycle = 12
    starving = 0
    maxStarving = 7
    maxAge = 25

    def performAction(self):
        '''Performs the action specific to the class Mouse'''
        self.age += 1
        self.starving += 1
        if self.age == self.maxAge or self.starving == self.maxStarving:
            self.world.delObj(self)
        if self.age % self.offspringCycle == 0 and self.age != 0:
            self.world.addNeighbor(self)
        directionOfCorn = self.detectCorn()
        if directionOfCorn != 255:
            self.feed(directionOfCorn)

    def detectCorn(self):
        '''Detects if there is corn in the direct neighborhood'''
        directions = [0, 1, 2, 3]
        random.shuffle(directions)
        for direction in directions:
            if type(self.world.getNeighbor(self.pos[0], self.pos[1],\
                    direction)) is Corn:
                return direction
        return 255

    def feed(self, directionOfCorn):
        '''Moves the Mouse in the given directionOfCorn and resets the starving'''
        self.world.move(self, directionOfCorn)
        self.starving = 0
