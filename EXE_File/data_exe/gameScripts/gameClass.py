import time
from copy import deepcopy
import keyboard


from TankScripts.tankSettings import tankSettings
from TankScripts.sensorClass import Box
from gameScripts.gameSettings import GameSettings
from SpawnScripts.SettingsClass import SettingsMap
import random as rnd

from gameScripts import gameSettings


def loadBest(visible):
    try:
        for line in range(visible * 2 + 1):
            lineWeights = []
            for box in range(visible * 2 + 1):
                b = Box()
                f = open(f"weightBestTank/{line}.{box}.txt", "r")
                lines = f.readlines()
                for sensor in range(3):
                    l = lines[sensor].split()
                    for side in range(4):
                        b[sensor][side] = int(l[side])
                lineWeights.append(b)
            tankSettings.matrixWeights.append(lineWeights)
    except FileNotFoundError:
        pass
class Game:
    def __init__(self, members, map, window, bonusAdd):
        self.members = members
        self.maxId = len(self.members)+1
        self.map = map
        self.window = window
        self.bonusHelth = bonusAdd
        self.addingBonus = SettingsMap.bonusUp
        self.visible = tankSettings.visibleZone
        self.maxMembers = SettingsMap.maxMembers
        self.walls = []
        self.bonuses = set()


        for y in range(len(map)):
            for x in range(len(map)):
                if map[y][x] == "W":
                    self.walls.append((x,y))
                elif map[y][x] == "B":
                    self.bonuses.add((x,y))

        self.game()

    def game(self):
        choices = 0
        while len(self.members) >0 and GameSettings.session==True:
            self.fires = []
            choices +=1
            if len(self.bonuses)< SettingsMap.bonuses:

                self.spawnBonus()

            newMap = deepcopy(self.map)

            hp = tankSettings.health

            for m in self.members:

                m.map = self.createVisibleZone(m.position, newMap)
                if m.health <=0:
                    continue

                if gameSettings.GameSettings.difficult != 0 and m.id != tankSettings.playerID:
                    m.checkFire()




                if m.id == tankSettings.playerID:
                    self.window.updateMatrix(newMap)

                    m.oldPos = deepcopy(m.position)
                    visibleZone = self.createVisibleZone(m.position, newMap)


                    hp = m.health
                    m.fire = "None"
                    if gameSettings.GameSettings.difficult == 1:
                        m.checkFire()

                    while GameSettings.session == True:
                        if keyboard.is_pressed("a"):
                            self.window.updateSide(tankSettings.playerID, "left")
                            newPos = (m.position [0] - 1, m.position[1])
                            break
                        elif keyboard.is_pressed("w"):
                            self.window.updateSide(tankSettings.playerID, "up")
                            newPos = (m.position[0], m.position[1] - 1)
                            break
                        elif keyboard.is_pressed("d"):
                            self.window.updateSide(tankSettings.playerID, "right")
                            newPos = (m.position[0] + 1, m.position[1])
                            break
                        elif keyboard.is_pressed("s"):
                            self.window.updateSide(tankSettings.playerID, "down")
                            newPos = (m.position[0], m.position[1] + 1)

                            break

                        if keyboard.is_pressed("up"):
                            m.fire = "up"

                        if keyboard.is_pressed("down"):
                            m.fire = "down"
                        if keyboard.is_pressed("left"):
                            m.fire = "left"
                        if keyboard.is_pressed("right"):
                            m.fire = "right"

                        self.window.update()

                    m.position = newPos
                    time.sleep(0.1)
                else:

                    m.oldPos =deepcopy( m.position)
                    m.choice(self.createVisibleZone(m.position, newMap))
                    newPos = m.position




                if self.checkChoice(newPos):
                    self.map[m.oldPos[1]][m.oldPos[0]] = 0
                    self.map[newPos[1]][newPos[0]] = m.id
                else:
                    m.position = m.oldPos

                if self.checkBonus(newPos):
                    m.health+= round(self.bonusHelth)

            for m in self.members:
                fire = self.fire(m.oldPos, m.id, m.fire, self.map)
                if fire:
                    self.removeHealth(fire, m.id)

            if gameSettings.GameSettings.difficult !=0:
                self.window.canvas.itemconfig(self.window.healthText,text=f"{hp}")
            self.window.canvas.itemconfig(self.window.choisesText, text=choices)


            self.checkMap()
            self.checkMembers()





        self.members.clear()
    def spawnBonus(self):
        size = len(self.map)
        x = rnd.randint(1, size - 2)
        y = rnd.randint(1, size - 2)
        o = self.map[y][x]
        c = 0
        while (str(o).isdigit()==False or int(o) > 0) and c<size :
            c+=1
            x = rnd.randint(1, size - 2)
            y = rnd.randint(1, size - 2)
            o = self.map[y][x]
        if c >= size:
            return

        self.bonuses.add((x,y))
        self.map[y][x] = "B"
    def checkChoice(self, newPos):

        if newPos in self.walls:
            return False
        elif newPos[0] <= -1 or newPos[0] >= len(self.map):
            return False
        elif newPos[1] <= -1 or newPos[1] >= len(self.map):
            return False
        return True


    def createVisibleZone(self, pos, oldMap):
        x,y = pos

        visibleMap = []
        for yT in range(y - self.visible, y+self.visible+1):
            visibleLine = []
            for xT in range(x - self.visible, x+self.visible+2):
                if xT <= -1 or xT >= len(self.map) or yT <=-1 or yT >=len(self.map):
                    if oldMap[y][x] == -1:
                        visibleLine.append("W")
                    else:
                        visibleLine.append(-1)
                else:
                    visibleLine.append(oldMap[yT][xT])
            visibleMap.append(visibleLine)

        return visibleMap



    def checkBonus(self, coord):
        if coord in self.bonuses:
            self.bonuses.remove(coord)
            return True
        return False

    def checkMap(self):
        for m in self.members:
            if m.health <= 0:
                continue
            for mem2 in self.members:
                if m == mem2 or mem2.health<=0:
                    continue
                if m.position == mem2.position:
                    m.health = 0
                    mem2.health = 0
                    if m.id==tankSettings.playerID or mem2.id == tankSettings.playerID:
                        GameSettings.win = None

                        self.window.endScreen(self.map)
                        GameSettings.session = False

                        return



    def checkMembers(self):
        newMem = []
        for m in self.members:
            if m.health > 0:
                newMem.append(m)
            elif m.id == tankSettings.playerID:
                GameSettings.session = False
                self.window.endScreen(self.map, self.fires)
                return True
            else:
                self.map[m.position[1]][m.position[0]] = 0
        self.members = newMem
        if len(self.members) == 1:
            GameSettings.win = True

            self.window.endScreen(self.map)
            return True
    def removeHealth(self, idRemove, idAdd):

        for tank in self.members:
            if idRemove == tank.id:
                tank.health -=50
            if idAdd == tank.id:
                tank.health +=25


    def fire(self, position, id, side, map):
        if side == "None":
            return False
        elif side == "left":

            for x in range(position[0]-1, position[0]-self.visible-1,-1):
                if x < 0:
                    continue
                if map[position[1]][x] == id:
                    continue
                if (type(map[position[1]][x]) == type(int())) and (map[position[1]][x] > 0):
                    return map[position[1]][x]
                self.fires.append((x, position[1]))
                self.window.setFire(x, position[1])
            return False
        elif side == "right":
            for x in range(position[0] +1, position[0] + self.visible + 1):

                if x >= len(map):
                    continue
                if map[position[1]][x] == id:
                    continue

                elif (type(map[position[1]][x]) == type(int())) and (
                        map[position[1]][x] > 0):
                    return map[position[1]][x]
                self.fires.append((x, position[1]))
                self.window.setFire(x,position[1])
            return False

        elif side == "down":
            for y in range(position[1] +1, position[1] + self.visible + 1):
                if y >= len(map):
                    continue
                if map[y][position[0]] == id:
                    continue

                elif (type(map[y][position[0]]) == type(int())) and (
                        map[y][position[0]] > 0 ):
                    return map[y][position[0]]
                self.fires.append((position[0], y))
                self.window.setFire(position[0], y)
            return False
        elif side == "up":
            for y in range(position[1] -1, position[1] - self.visible - 1,-1):
                if y < 0:
                    continue
                if map[y][position[0]] == id:
                    continue

                if (type(map[y][position[0]]) == type(int())) and (map[y][position[0]] > 0 ):

                    return map[y][position[0]]
                self.fires.append((position[0], y))
                self.window.setFire(position[0], y)
            return False













