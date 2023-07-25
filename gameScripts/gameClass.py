from copy import deepcopy


import TankScripts.tankClass
from TankScripts.tankSettings import tankSettings
from TankScripts.tankClass import Tank
from SpawnScripts.SettingsClass import SettingsMap
import random as rnd


def loadBest(visible):
    try:
        info = open("weightBestTank/info.txt", "r")
        lines = info.readlines()
        tankSettings.chanceMutation = int(lines[1])
        tankSettings.valueMutaion = int(lines[2])
        tankSettings.health = int(lines[3]) // 2
        tankSettings.mutation = int(lines[4])
        info.close()
        for line in range(visible * 2 + 1):
            lineWeights = []
            for box in range(visible * 2 + 1):
                b = TankScripts.tankClass.Box()
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
        self.bonuses = []


        for y in range(len(map)):
            for x in range(len(map)):
                if map[y][x] == "W":
                    self.walls.append((x,y))
                elif map[y][x] == "B":
                    self.bonuses.append((x,y))

        self.game()

    def game(self):
        self.choices = 0

        counter = 0
        while len(self.members) >0:
            print(len(self.members), self.choices)
            if self.choices >= 10000 and SettingsMap.bonuses > 20:
                self.choices = 0
                self.bonusHelth+=self.addingBonus
                SettingsMap.bonuses = SettingsMap.bonuses-10
                counter+=1
                with open("information.txt","a") as file:
                    file.write(str(10000*counter)+" choices\n")
                    file.write("Population: "+str(len(self.members))+"\n")
                    file.write("BONUS_ADD: "+str(round(self.bonusHelth))+"\n")
                    file.write("BONUSES: "+str(SettingsMap.bonuses)+"\n\n")

                    file.close()
                print(10000*counter,"choices")
                print("Population:", len(self.members))
                print("BONUSES:", SettingsMap.bonuses)
                print("BONUS_ADD: ", self.bonusHelth)
                self.saveBest()
            self.choices+=1

            while len(self.bonuses) < SettingsMap.bonuses:
                self.spawnBonus()
            newMap = deepcopy(self.map)
            for m in self.members:

                m.health = m.health - 1
                pos = m.position
                m.choice(self.createVisibleZone(m.position, newMap))
                newPos = m.position
                if newPos == m.oldPos or pos == m.oldPos:
                    if m.countOldPos == 3:
                        m.health=0
                    m.countOldPos += 1
                else:
                    m.countOldPos = 0
                if self.checkChoice(newPos):
                    self.map[pos[1]][pos[0]] = 0
                    self.map[newPos[1]][newPos[0]] = m.id
                else:
                    m.position = pos
                m.oldPos = pos

                if self.checkBonus(newPos):
                    m.health+= round(self.bonusHelth)

                if m.health >= m.healthSpawnTank:
                    m.health = m.health - 100
                    self.spawnTank(m)

            '''
            self.window.choices = self.choices
            self.window.bestLife = self.spawns
            self.window.bestMutation = self.mutation
            self.window.tanks = len(self.members)
            self.window.costChoice = SettingsMap.removeHealth
            self.window.bonuses = len(self.bonuses)
            self.window.updateMatrix(self.map)


            '''

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
        self.bonuses.append((x,y))
        self.map[y][x] = "B"
    def checkChoice(self, newPos):

        if newPos in self.walls:
            return False
        elif newPos[0] <= -1 or newPos[0] >= len(self.map)-1:
            return False
        elif newPos[1] <= -1 or newPos[1] >= len(self.map)-1:
            return False
        return True

    def spawnTank(self, tankFather):
        size = len(self.map)
        x = rnd.randint(1, size - 2)
        y = rnd.randint(1, size - 2)
        o = self.map[y][x]
        c = 0
        while ((str(o) != "0" and str(o) !="B") or any(map(lambda t:self.checkPosition(t.position, (x,y)), self.members))) and c<size:
            c+=1
            x = rnd.randint(1, size - 2)
            y = rnd.randint(1, size - 2)
            o = self.map[y][x]
        if c >= size:
            return
        self.map[y][x] = self.maxId
        tankFather.spawns +=1
        tank = Tank(self.maxId, (x,y), self.window, gens=tankFather.matrixWeights, mutaion=tankFather.mut, chanceMutation=tankFather.chanceMutation, valueMutaion=tankFather.valueMutaion)
        self.maxId+=1
        self.members.append(tank)


    def createVisibleZone(self, pos, oldMap):
        x,y = pos
        visibleMap = []
        for yT in range(y - self.visible, y+self.visible+1):
            visibleLine = []
            for xT in range(x - self.visible, x+self.visible+1):
                if xT <= -1 or xT >= len(self.map) or yT <=-1 or yT >=len(self.map):
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
                if self.checkPosition(m.position, mem2.position):
                    if m.health > mem2.health:
                        m.health += mem2.health
                        mem2.health = 0
                    elif m.health < mem2.health:
                        mem2.health+=m.health
                        m.health = 0
                    else:
                        m.health = 0
                        mem2.health = 0
                if m.position == mem2.position:

                    m.health = 0

    def checkMembers(self):
        newMem = []
        for m in self.members:

            if m.health > 0:
                newMem.append(m)
            else:
                self.map[m.position[1]][m.position[0]] = 0
        self.members = newMem

    def checkPosition(self, position, position2):
        if position[0] == position2[0] and abs(position[1] - position2[1]) == 1:
            return True
        if position[1] == position2[1] and abs(position[0] - position2[0]) == 1:
            return True
        return False

    def saveBest(self):
        best = max( self.members, key=lambda x:x.spawns)
        print("MUTATION:", best.mut)
        try:
            info = open("weightBestTank/info.txt","x")
            info.write("0")
            info.close()
        except FileExistsError:
            pass
        for lineWeight in range(self.visible*2+1):
            for box in range(self.visible*2+1):
                for sensor in range(len(best.matrixWeights[lineWeight][box])):
                    minSide = min(best.matrixWeights[lineWeight][box][sensor])
                    for side in range(4):
                        best.matrixWeights[lineWeight][box][sensor][side] =best.matrixWeights[lineWeight][box][sensor][side] - minSide

        info = open("weightBestTank/info.txt", "w")
        info.write(str(best.spawns)+"\n")
        info.write(str(best.chanceMutation)+"\n")
        info.write(str(best.valueMutaion)+"\n")
        info.write(str(best.healthSpawnTank)+"\n")
        info.write(str(best.mut)+"\n")
        info.close()
        for line in range(self.visible*2+1):
            for box in range(self.visible*2+1):
                f = open(f"weightBestTank/{line}.{box}.txt", "w")
                for sensor in best.matrixWeights[line][box]:
                    f.write(str(sensor)+"\n")
                f.close()









