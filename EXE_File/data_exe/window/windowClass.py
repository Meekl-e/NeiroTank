import time
from tkinter import *
from copy import deepcopy

import gameScripts.gameSettings
from SpawnScripts.SettingsClass import SettingsMap
from TankScripts.tankSettings import tankSettings
from gameScripts.gameSettings import GameSettings

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
        self.sprites["gameScreen"] = PhotoImage(file="sprites/gameScreen.png")
        self.sprites["winScreen"] = PhotoImage(file="sprites/win.png")
        self.sprites["endScreen"] = PhotoImage(file="sprites/end.png")
        self.sprites["endNoneScreen"] = PhotoImage(file="sprites/noneEnd.png")

    def loadRecords(self):
        file = open("data/records.txt","r")
        self.records = list(map(int, file.readlines()))
        file.close()

    def saveRecords(self):
        file = open("data/records.txt", "w")
        file.writelines([str(r)+"\n" for r in self.records])
        file.close()




    def __init__(self, size):
        super().__init__()
        self.size = size
        #self.overrideredirect(1)
        #self.state('zoomed')
        self.geometry("1536x864-100-100")
        self.resizable(width=False, height=False)
        self.config(background="palegreen3")
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
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


        # АПодгружаем спарйты
        self.loadSprites()
        self.loadRecords()
        self.draw_interface()


    def draw_interface(self):
        nameProject = Label(text="НЕЙРОТАНК", font=("Softie Cyr", 100, "bold"), bg="palegreen3")
        nameProject.pack(fill=X)

        menuFrame = Frame(self, width=1536, borderwidth=0, background="palegreen3")
        menuFrame.pack(fill=X)
        gameFrame = Frame(menuFrame, width=50 * 10 * 2, borderwidth=0, background="palegreen3")
        gameFrame.pack(side=LEFT)
        for x in range(self.size):
            frame = Frame(gameFrame, width=self.size, borderwidth=0)
            frame.pack(side=TOP)
            lineMatrix = []
            for y in range(self.size):
                l = Label(frame, height=50, width=50, borderwidth=2, relief=GROOVE)
                lineMatrix.append(l)
                l.pack(side=LEFT)
            self.matrixLabels.append(lineMatrix)
        self.canvas = Canvas(menuFrame, width=884, height=643, bg="palegreen3", cursor="target", borderwidth=0,)
        self.canvas.pack(side=LEFT, fill=Y)
        self.screenImg = self.canvas.create_image(0, 0, image=self.sprites["gameScreen"], anchor=NW)
        self.canvas.create_rectangle(397, 543, 884, 643, activefill="yellow", width=0)

        self.healthText = self.canvas.create_text(275, 385, text=f"{tankSettings.health}", font=("Softie Cyr", 33), anchor=W, fill="#2a2a2a")
        self.choisesText =self.canvas.create_text(500, 471, text="0", font=("Softie Cyr", 33), anchor=W, fill="#2a2a2a")

        self.canvas.bind("<Button-1>", self.mouseBind)
        if gameScripts.gameSettings.GameSettings.difficult == 0:
            self.canvas.itemconfig(self.healthText, text="∞")
        else:
            self.textRecord = Label(self, text=f"Рекорд шагов для победы в данной сложности: {self.records[GameSettings.difficult-1]}", font=("Softie Cyr", 33),
                                    bg="palegreen3")
            self.textRecord.pack()







    def updateSide(self, idTank, side):
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix)):
                if self.matrix[y][x] != idTank:
                    continue

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

    def on_closing(self):
        self.destroy()
        GameSettings.work = False
        GameSettings.In_menu = False
        GameSettings.session = False


    def mouseBind(self, event):
        # (397, 543, 884, 643,
        if 397 <= event.x <= 884 and 543 <= event.y <= 643:
            self.destroy()
            GameSettings.session = False
            GameSettings.endGame = False

    def endScreen(self, matrix, fires=[]):

        self.updateMatrix(matrix)

        self.canvas.itemconfig(self.healthText, text="")
        self.canvas.moveto(self.choisesText, 500, 365)
        if GameSettings.win == True:
            self.canvas.itemconfig(self.screenImg, image=self.sprites["winScreen"])
            choises = int(self.canvas.itemcget(self.choisesText, option="text"))
            if choises < self.records[GameSettings.difficult - 1]:
                self.textRecord.config(text="Новый рекорд: " + str(choises))
                self.records[GameSettings.difficult - 1] = choises
                self.saveRecords()
        elif GameSettings.win == False:
            for f in fires:
                self.setFire(*f)
            self.canvas.itemconfig(self.screenImg, image=self.sprites["endScreen"])
        else:
            self.canvas.itemconfig(self.screenImg, image=self.sprites["endNoneScreen"])


        GameSettings.endGame = True
        while GameSettings.endGame:
            self.update()





















