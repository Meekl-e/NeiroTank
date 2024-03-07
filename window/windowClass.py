import time
from tkinter import *
from copy import deepcopy

import gameScripts.gameSettings
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
        self.overrideredirect(1)
        self.state('zoomed')
        self.geometry("1536x864")
        self.resizable(width=False, height=False)

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

        nameProject = Label( text="НЕЙРОТАНК", font=("Softie Cyr", 100, "bold"), bg="palegreen3")
        nameProject.pack(fill=X)

        menuFrame = Frame(self, width=self.winfo_screenwidth())
        menuFrame.pack(fill=X)
        gameFrame = Frame(menuFrame, width=50*10*2)
        gameFrame.pack(side=LEFT)
        for x in range(size):
            frame = Frame(gameFrame, width=size)
            frame.pack(side=TOP)
            lineMatrix = []
            for y in range(size):
                l = Label(frame, height=50, width=50, borderwidth=2, relief=GROOVE  )
                lineMatrix.append(l)
                l.pack(side=LEFT)
            self.matrixLabels.append(lineMatrix)
        if gameScripts.gameSettings.GameSettings.difficult != 0:
            self.healthT = Label(self, width=size, text=f"Здоровье: {tankSettings.health}", font=("Georgia", 20) )
            self.healthT.pack()
        canvas = Canvas(menuFrame, width=self.winfo_screenwidth()-size, height=50*10, bg="black")
        canvas.pack(side=LEFT, fill=Y)


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
                        self.tanksSprites[idTank] = self.sprites["playerRight"]
                    elif side == "left":
                        self.tanksSprites[idTank] = self.sprites["playerLeft"]
                    elif side == "down":
                        self.tanksSprites[idTank] = self.sprites["playerDown"]
                    else:
                        self.tanksSprites[idTank] = self.sprites["playerUp"]
                    return
                else:
                    if side == "right":
                        self.tanksSprites[idTank] = self.sprites["enemyRight"]
                    elif side == "left":
                        self.tanksSprites[idTank] = self.sprites["enemyLeft"]
                    elif side == "down":
                        self.tanksSprites[idTank] = self.sprites["enemyDown"]
                    else:
                        self.tanksSprites[idTank] = self.sprites["enemyUp"]
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
                elif o == tankSettings.playerID or o == -1:
                    if self.tanksSprites.get(o) is None:
                        self.tanksSprites[o] = self.sprites["playerUp"]
                    self.matrixLabels[y][x].config(image=self.tanksSprites[o])
                else:
                    if self.tanksSprites.get(o) is None:
                        self.tanksSprites[o] = self.sprites["enemyUp"]
                    self.matrixLabels[y][x].config(image=self.tanksSprites[o])

        self.update()

    def setFire(self, x,y):
        self.matrixLabels[y][x].config(image=self.sprites["fire"])
        self.update()













