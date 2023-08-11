import random

from TankScripts.tankSettings import tankSettings



class Tank:
    def __init__(self, id, position, window, NN  ):
        self.neuralNetwork = NN
        self.health = tankSettings.health
        self.position = position
        self.window = window

        self.fire = "None"
        self.lenMap = tankSettings.visibleZone*2+1
        self.id = id
        self.randomSide  = (False, 0)
        self.activeSensors = []


        self.healthSpawnTank = 100
        self.matrixWeights = tankSettings.matrixWeights



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

        self.setCoords(self.getSide())

    def checkFire(self):

        self.fire = random.choice(["right","left","up","down"])#self.neuralNetwork.predict(self.map)
        return self.fire


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

        self.window.updateSide(self.id, side)
        if side=="right":
            self.position = (x+1, y)
        elif side=="up":
            self.position = (x, y-1)
        elif side=="left":
            self.position = (x-1, y)
        elif side=="down":
            self.position = (x, y+1)





