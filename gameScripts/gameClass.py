import time
from copy import deepcopy
import keyboard

import TankScripts.tankClass
from TankScripts.tankSettings import tankSettings
from TankScripts.sensorClass import Box
from TankScripts.AIfire import check_fire
from SpawnScripts.SettingsClass import SettingsMap
import random as rnd


def loadBest(visible):
    try:
        info = open("weightBestTank/info.txt", "r")
        lines = info.readlines()
        SettingsMap.choices = int(lines[0])
        SettingsMap.counter = int(lines[1])
        tankSettings.health = int(lines[4]) // 2

        info.close()
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
        self.choices = 0

        self.counter = SettingsMap.counter
        while len(self.members) >0:


            if len(self.bonuses)< SettingsMap.bonuses:

                self.spawnBonus()

            newMap = deepcopy(self.map)
            hp=100

            for m in self.members:


                if m.health <=0:
                    continue

                if m.id == tankSettings.playerID:
                    self.window.updateMatrix(newMap)
                    pos = m.position
                    visibleZone = self.createVisibleZone(m.position, newMap)
                    #self.createVisibleZone(m.position, newMap))
                    hp = m.health

                    while True:
                        if keyboard.is_pressed("a"):
                            self.window.updateSide(tankSettings.playerID, "left")
                            newPos = (pos[0] - 1, pos[1])
                            break
                        elif keyboard.is_pressed("w"):
                            self.window.updateSide(tankSettings.playerID, "up")
                            newPos = (pos[0], pos[1] - 1)
                            break
                        elif keyboard.is_pressed("d"):
                            self.window.updateSide(tankSettings.playerID, "right")
                            newPos = (pos[0] + 1, pos[1])
                            break
                        elif keyboard.is_pressed("s"):
                            self.window.updateSide(tankSettings.playerID, "down")
                            newPos = (pos[0], pos[1] + 1)
                            break

                        if keyboard.is_pressed("up"):
                            m.fire = "up"
                        elif keyboard.is_pressed("down"):
                            m.fire = "down"
                        elif keyboard.is_pressed("left"):
                            m.fire = "left"
                        elif keyboard.is_pressed("right"):
                            m.fire = "right"
                        self.window.update()

                    m.position = newPos
                    time.sleep(0.05)
                else:

                    pos = m.position
                    m.choice(self.createVisibleZone(m.position, newMap))

                    newPos = m.position




                if self.checkChoice(newPos):
                    self.map[pos[1]][pos[0]] = 0
                    self.map[newPos[1]][newPos[0]] = m.id
                else:
                    m.position = pos
               # m.checkFire()
                #fire = self.fire(m.position, m.id, m.fire, newMap)
                #if fire:
                 #   self.removeHealth(fire, m.id)

                if self.checkBonus(newPos):
                    m.health+= round(self.bonusHelth)


            self.window.healthT.config(text=f"XP: {hp}")

            self.checkMap()
            if self.checkMembers():
                self.window.destroy()
                return



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



    def checkMembers(self):
        newMem = []
        for m in self.members:
            if m.health > 0:
                newMem.append(m)
            elif m.id == tankSettings.playerID:
                return True
            else:
                self.map[m.position[1]][m.position[0]] = 0
        self.members = newMem

    def removeHealth(self, idRemove, idAdd):
        print(idRemove, idAdd)
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
                if (type(map[position[1]][x]) == type(int())) and (map[position[1]][x] > 0 or map[position[1]][x] == -1):
                    return map[position[1]][x]
                self.window.setFire(x, position[1])
            return False
        elif side == "right":
            for x in range(position[0] + 1, position[0] + self.visible + 1):

                if x >= len(map):
                    continue
                if map[position[1]][x] == id:
                    continue

                elif (type(map[position[1]][x]) == type(int())) and (
                        map[position[1]][x] > 0 or map[position[1]][x] == -1):
                    return map[position[1]][x]
                self.window.setFire(x,position[1])
            return False

        elif side == "down":
            for y in range(position[1] + 1, position[1] + self.visible + 1):
                if y >= len(map):
                    continue
                if map[y][position[0]] == id:
                    continue

                elif (type(map[y][position[0]]) == type(int())) and (
                        map[y][position[0]] > 0 or map[y][position[0]] == -1):
                    return map[y][position[0]]
                self.window.setFire(position[0], y)
            return False
        elif side == "up":
            for y in range(position[1] - 1, position[1] - self.visible - 1,-1):
                if y < 0:
                    continue
                if map[y][position[0]] == id:
                    continue

                if (type(map[y][position[0]]) == type(int())) and (map[y][position[0]] > 0 or map[y][position[0]] == -1):

                    return map[y][position[0]]
                self.window.setFire(position[0], y)
            return False













