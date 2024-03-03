import time
from tkinter import *
from copy import deepcopy

from SpawnScripts.SettingsClass import SettingsMap
from TankScripts.tankSettings import tankSettings


# E - enemy
# P - player
# B - bonus
# W - wall (стена)



class Window(Tk):

    def loadSprites(self):
        self.sprites["enemyUp"] = PhotoImage(file="sprites/enemySpriteUp.png", )
        self.sprites["enemyLeft"] = PhotoImage(file="sprites/enemySpriteLeft.png", )
        self.sprites["enemyDown"] = PhotoImage(file="sprites/enemySpriteDown.png", )
        self.sprites["enemyRight"] = PhotoImage(file="sprites/enemySpriteRight.png", )
        self.sprites["playerUp"] = PhotoImage(file="sprites/playerUpSprite.png", )
        self.sprites["playerRight"] = PhotoImage(file="sprites/playerRightSprite.png", )
        self.sprites["playerDown"] = PhotoImage(file="sprites/playerDownSprite.png", )
        self.sprites["playerLeft"] = PhotoImage(file="sprites/playerLeftSprite.png", )
        self.sprites["bonus"] = PhotoImage(file="sprites/bonusSprite.png", )
        self.sprites["wall"] = PhotoImage(file="sprites/wallSprite.png", )
        self.sprites["path"] = PhotoImage(file="sprites/pathSprite.png", )
        self.sprites["fire"] = PhotoImage(file="sprites/pathFireSprite.png", )


    def __init__(self, size):
        super().__init__()
        self.choices = 0
        self.bestLife = 0
        self.tanks = 0
        self.bestMutation = 0
        self.bonuses = SettingsMap.bonuses
        self.costChoice = SettingsMap.removeHealth
        self.sprites = {}
        self.title("Танки")
        #self.geometry(f"{size**2}x{size**2}")
        self.matrixLabels = []
        self.tanksSprites = {}
        self.matrix = [([0]*size).copy() for i in range(size)]
        for x in range(size):
            frame = Frame(self, width=size)
            frame.pack(fill=X)
            lineMatrix = []
            for y in range(size):
                l = Label(frame, height=25, width=25, borderwidth=2, relief=GROOVE  )
                lineMatrix.append(l)
                l.pack(side=LEFT)
            self.matrixLabels.append(lineMatrix)
        self.healthT = Label(self, width=size, text="XP: 100", font=("Georgia", 20) )
        self.healthT.pack()


        # АПодгружаем спарйты
        self.loadSprites()



    def updateSide(self, idTank, side):
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix)):
                if self.matrix[y][x] != idTank:
                    continue
                print(tankSettings.playerID)
                if idTank == tankSettings.playerID:
                    if side == "right":
                        self.tanksSprites[idTank] = self.sprites["enemyRight"]
                    elif side == "left":
                        self.tanksSprites[idTank] = self.sprites["enemyLeft"]
                    elif side == "down":
                        self.tanksSprites[idTank] = self.sprites["enemyDown"]
                    else:
                        self.tanksSprites[idTank] = self.sprites["enemyUp"]
                    return
                else:
                    if side == "right":
                        self.tanksSprites[idTank] = self.sprites["playerRight"]
                    elif side == "left":
                        self.tanksSprites[idTank] = self.sprites["playerLeft"]
                    elif side == "down":
                        self.tanksSprites[idTank] = self.sprites["playerDown"]
                    else:
                        self.tanksSprites[idTank] = self.sprites["playerUp"]
                    return

    def updateMatrix(self, newMatrix):
        global c
        self.matrix = deepcopy(newMatrix)
        for y in range(len(newMatrix)):
            for x in range(len(newMatrix)):
                o = newMatrix[y][x]
                if o == 0:
                    self.matrixLabels[y][x].config(image=self.sprites["path"])
                elif o == "B":
                    self.matrixLabels[y][x].config(image=self.sprites["bonus"])
                elif o == "W":
                    self.matrixLabels[y][x].config(image=self.sprites["wall"])
                elif o > 0:
                    if self.tanksSprites.get(o) is None:
                        self.tanksSprites[o] = self.sprites["playerUp"]
                    self.matrixLabels[y][x].config(image=self.tanksSprites[o])
                elif o ==tankSettings.playerID or o==-1:
                    if self.tanksSprites.get(o) is None:
                        self.tanksSprites[o] = self.sprites["enemyUp"]
                    self.matrixLabels[y][x].config(image=self.tanksSprites[o])

        self.update()

    def setFire(self, x,y):
        self.matrixLabels[y][x].config(image=self.sprites["fire"])
        self.update()






c = 0






