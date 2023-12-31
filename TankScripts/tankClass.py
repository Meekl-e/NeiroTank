import random
import time

from TankScripts.sensorClass import Box
from TankScripts.tankSettings import tankSettings
from TankScripts.tankMainFire import CheckTank


class Tank:
    def __init__(self, id, position, window, gens=[], mutaion=0, chanceMutation =tankSettings.chanceMutation, valueMutaion = tankSettings.valueMutaion ):

        self.health = tankSettings.health #healthSpawn//2
        self.oldPos = ()
        self.countOldPos = 0
        self.mut = mutaion
        self.spawns = 0
        self.position = position
        self.matrixWeights = []
        self.window = window
        self.lenMap = tankSettings.visibleZone*2+1
        self.id = id
        self.randomSide = (False,0)
        self.activeSensors = []

        self.chanceMutation = chanceMutation
        self.valueMutaion = valueMutaion
        self.healthSpawnTank = 100
        if gens == []:

            self.createWeights()
        else:
            self.matrixWeights = gens
        self.mutation()

    def createWeights(self):
        if tankSettings.matrixWeights:
            self.matrixWeights =tankSettings.matrixWeights
            return
        for y in range(self.lenMap):
            lineWeights = []
            for x in range(self.lenMap):
                lineWeights.append(Box(random=3))
            self.matrixWeights.append(lineWeights)


    def mutation(self):
        for line in range(len(self.matrixWeights)):
            for weight in range(len(self.matrixWeights[line])):
                if random.randint(1,self.chanceMutation) == 1:
                    self.mut += 1
                    for box in range(len(self.matrixWeights[line][weight])):
                        for side in range(4):
                            self.matrixWeights[line][weight][box][side] = self.matrixWeights[line][weight][box][side] + random.randint(-self.valueMutaion,self.valueMutaion)


        #print(self.matrixWeights)



    def choice(self, map):

        self.map = map

        if self.randomSide[0]:

            if self.randomSide[1] == "left":
                for x,y,type in self.activeSensors:
                    self.matrixWeights[y][x].getSensorOfType(type).left +=1
            elif self.randomSide[1] == "right":
                for x,y,type in self.activeSensors:

                    self.matrixWeights[y][x].getSensorOfType(type).right += 1
            elif self.randomSide[1] == "up":
                for x,y,type in self.activeSensors:

                    self.matrixWeights[y][x].getSensorOfType(type).up += 1
            else:
                for x,y,type in self.activeSensors:

                    self.matrixWeights[y][x].getSensorOfType(type).down += 1
            self.randomSide = (False,0)



     #   if self.test == None:
      #      if random.randint(0,200) == 1:
       #         self.test = CheckTank(map)
        #else:
         #   self.test.saveChoice(map)
          #  self.test = None

        #print(self.map)
       # for l in self.map:
         #   print(l)
        #print(self.getSide())

        self.setCoords(self.getSide())


    def getSide(self):
        sides = {"right":0, "left":0,"down":0, "up":0}
        self.activeSensors = []
        for y in range(self.lenMap):
            for x in range(self.lenMap):
                if x == (self.lenMap-1)//2 and y == (self.lenMap-1)//2:
                    continue
                control= self.matrixWeights[y][x].getSensor(self.map[y][x])
                if control.type != "":
                    self.activeSensors.append((x,y, control.type))
                sides["right"] += control.right
                sides["left"] += control.left
                sides["up"] += control.up
                sides["down"] += control.down
        sides = zip(sides.keys(), sides.values())
        s = sorted(sides, key=lambda x:x[1], reverse=True)

        if s[0][1] == s[1][1] == s[2][1] == s[3][1]:
            self.randomSide = (True,random.choice(s)[0])
            return self.randomSide[1]
        if s[0][1] == s[1][1] == s[2][1]:
            self.randomSide = (True, random.choice(s[:3])[0])
            return self.randomSide[1]
        if s[0][1] == s[1][1]:
            self.randomSide = (True, random.choice(s[:2])[0])
            return self.randomSide[1]
        self.randomSide = (False,0)
        return s[0][0]
    def setCoords(self, side):

        x,y = self.position

#        self.window.updateSide(self.id, side)
        if side=="right":
            self.position = (x+1, y)
        elif side=="up":
            self.position = (x, y-1)
        elif side=="left":
            self.position = (x-1, y)
        elif side=="down":
            self.position = (x, y+1)




