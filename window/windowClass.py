from tkinter import *
from copy import deepcopy

from SpawnScripts.SettingsClass import SettingsMap





# E - enemy
# P - player
# B - bonus
# W - wall (стена)



class Window(Tk):

    def loadSprites(self):
        self.sprites["enemy"] = PhotoImage(file="sprites/enemySprite.png", )
        self.sprites["playerUp"] = PhotoImage(file="sprites/playerUpSprite.png", )
        self.sprites["playerRight"] = PhotoImage(file="sprites/playerRightSprite.png", )
        self.sprites["playerDown"] = PhotoImage(file="sprites/playerDownSprite.png", )
        self.sprites["playerLeft"] = PhotoImage(file="sprites/playerLeftSprite.png", )
        self.sprites["bonus"] = PhotoImage(file="sprites/bonusSprite.png", )
        self.sprites["wall"] = PhotoImage(file="sprites/wallSprite.png", )
        self.sprites["path"] = PhotoImage(file="sprites/pathSprite.png", )

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
        frame = Frame(self, width=size)
        frame.pack(fill=X)
        lC = Label(frame, text="ХОДЫ: ", font=("Arial", 11))
        lC.pack(side=LEFT)
        self.lCT = Label(frame, text=self.choices, font=("Arial", 11))
        self.lCT.pack(side=LEFT)
        lM = Label(frame, text="МУТ.: ")
        lM.pack(side=LEFT)
        self.lMT = Label(frame, text=self.bestMutation, font=("Arial", 11))
        self.lMT.pack(side=LEFT)
        lL = Label(frame, text="СОБРАНО: ")
        lL.pack(side=LEFT)
        self.lLT = Label(frame, text=self.bestLife, font=("Arial", 11))
        self.lLT.pack(side=LEFT)
        lT = Label(frame, text="ТАНКОВ: ")
        lT.pack(side=LEFT)
        self.lTT = Label(frame, text=self.tanks, font=("Arial", 11))
        self.lTT.pack(side=LEFT)
        lW = Label(frame, text="ЦЕНА ШАГА: ")
        lW.pack(side=LEFT)
        self.lWT = Label(frame, text=self.costChoice, font=("Arial", 11))
        self.lWT.pack(side=LEFT)
        lB = Label(frame, text="БОНУСОВ: ", font=("Arial", 11))
        lB.pack(side=LEFT)
        self.lBT = Label(frame, text=self.bonuses, font=("Arial", 11))
        self.lBT.pack(side=LEFT)

        frame = Frame(self, width=size)
        frame.pack(fill=X)
        l = Label(frame,text="БОНУСЫ: ")
        l.pack(side=LEFT)
        self.bonusField = Entry(frame,  font=("Arial", 11), cursor="hand2")
        self.bonusField.pack(side=LEFT)
        self.submitBonus = Button(frame, font=("Arial", 11, "bold"), text="ПОДТВЕРДИТЬ", cursor="hand2", command=self.setBonuses )
        self.submitBonus.pack(side=LEFT)

        frame = Frame(self, width=size)
        frame.pack(fill=X)
        l = Label(frame,text="УРОН ЗА ХОД: ")
        l.pack(side=LEFT)
        self.damageField = Entry(frame,  font=("Arial", 11), cursor="hand2")
        self.damageField.pack(side=LEFT)
        self.submitDamage = Button(frame, font=("Arial", 11, "bold"), text="ПОДТВЕРДИТЬ", cursor="hand2", command=self.setDamge )
        self.submitDamage = Button(frame, font=("Arial", 11, "bold"), text="ПОДТВЕРДИТЬ", cursor="hand2", command=self.setDamge )
        self.submitDamage.pack(side=LEFT)

        # АПодгружаем спарйты
        self.loadSprites()



    def updateSide(self, idTank, side):
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix)):
                if self.matrix[y][x] != idTank:
                    continue
                if side == "right":
                    self.tanksSprites[idTank] = self.sprites["playerRight"]
                elif side == "left":
                    self.tanksSprites[idTank] = self.sprites["playerLeft"]
                elif side == "down":
                    self.tanksSprites[idTank] = self.sprites["playerDown"]
                else:
                    self.tanksSprites[idTank] = self.sprites["playerUp"]


    def updateMatrix(self, newMatrix):
        self.matrix = deepcopy(newMatrix)
        for y in range(len(newMatrix)):
            for x in range(len(newMatrix)):
                o = newMatrix[y][x]
                if o == 0:
                    self.matrixLabels[y][x].config(image=self.sprites["path"])
                #elif o == "E":
                 #   self.matrixLabels[y][x].config(image=self.sprites["enemy"])
                #elif o == "P":
                 #   self.matrixLabels[y][x].config(image=self.sprites["player"])
                elif o == "B":
                    self.matrixLabels[y][x].config(image=self.sprites["bonus"])
                elif o == "W":
                    self.matrixLabels[y][x].config(image=self.sprites["wall"])
                elif o > 0:
                    if self.tanksSprites.get(o) is None:
                        self.tanksSprites[o] = self.sprites["playerUp"]
                    self.matrixLabels[y][x].config(image=self.tanksSprites[o])
        self.lCT.config(text=self.choices)
        self.lMT.config(text=self.bestMutation)
        self.lTT.config(text=self.tanks)
        self.lLT.config(text=self.bestLife)
        self.lWT.config(text=self.costChoice)
        self.lBT.config(text=self.bonuses)

        self.update()

    def setBonuses(self):
        SettingsMap.bonuses = int(self.bonusField.get())
    def setDamge(self):
        SettingsMap.removeHealth = int(self.damageField.get())








