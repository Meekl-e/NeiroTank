import time
from tkinter import *

from gameScripts.gameSettings import GameSettings
from window import windowClass
from SpawnScripts import mapClass
from gameScripts import gameClass
from SpawnScripts.SettingsClass import SettingsMap
from TankScripts.tankClass import Tank
from TankScripts.tankSettings import tankSettings


class startWindow(Tk):

    def __init__(self):
        super().__init__()
        self.difficult = 0
        self.tankSprite = PhotoImage(file="sprites/tankMenu.png")
        self.rulesImage =PhotoImage(file="sprites/rules.png")
        GameSettings.In_menu = True
        self.InRules = False
        self.canvas = Canvas(self, width=1536, height=864, bg="palegreen3", borderwidth=0,
                             cursor="target")
        self.canvas.pack()
        self.resizable(width=False, height=False)
        # self.overrideredirect(1)
        # self.state('zoomed')
        self.geometry("1536x864-100-100")
        self.draw_interface()

        self.canvas.bind("<Button-1>", self.mouse_touch)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.loop()

    def draw_interface(self):
        self.difficult = 0
        self.buttonDown = self.canvas.create_polygon(1100, 232, 1100, 632, 1500, 432, fill="red", )

        self.textStart = self.canvas.create_text(1100, 432, text="НАЧАТЬ", font=("Softie Cyr", 60, "bold"), anchor=W)
        self.buttonUp = self.canvas.create_polygon(1100, 232, 1100, 632, 1500, 432, fill="",
                                                   activefill="yellow", activeoutline="red", outline="")

        self.canvas.create_rectangle(0, 770, 400, 870, fill="red")
        self.canvas.create_text(200, 820, text="Правила", font=("Softie Cyr", 60, "bold"))
        self.canvas.create_rectangle(0, 770, 401, 870, fill="",
                                                    activefill="yellow", activeoutline="red", outline="")



        self.canvas.create_text(768, 70, text="НЕЙРОТАНК", font=("Softie Cyr", 100, "bold"))
        self.canvas.create_text(300, 160, text="Выбор уровня сложности:", font=("Softie Cyr", 30))

        self.canvas.create_text(150, 200, text="Демонстрационная сложность",
                                font=("Softie Cyr", 27), anchor=W)
        self.canvas.create_text(200, 240, text="1 противник, без стрельбы",
                                font=("Softie Cyr", 25), anchor=W)
        self.canvas.create_text(200, 270, text="Подходит для тех, кто просто хочет посмотреть на проект.",
                                font=("Softie Cyr", 25), anchor=W)

        self.canvas.create_text(150, 350, text="Легкая сложность",
                                font=("Softie Cyr", 27), anchor=W)
        self.canvas.create_text(200, 390,
                                text="Автострельба, 1 противник, много бонусов",
                                font=("Softie Cyr", 25), anchor=W)
        self.canvas.create_text(200, 420,
                                text="Для тех, кто хочет попробовать.",
                                font=("Softie Cyr", 25), anchor=W)

        self.canvas.create_text(150, 500, text="Средняя сложность",
                                font=("Softie Cyr", 27), anchor=W)
        self.canvas.create_text(200, 540,
                                text="1 противник, мало бонусов, немного здоровья",
                                font=("Softie Cyr", 25), anchor=W)
        self.canvas.create_text(200, 570,
                                text="Для тех, кто хочет испытать свои силы против ИИ",
                                font=("Softie Cyr", 25), anchor=W)

        self.canvas.create_text(150, 650, text="Очень сложная сложность",
                                font=("Softie Cyr", 27), anchor=W)
        self.canvas.create_text(200, 690,
                                text="5 противников, мало бонусов, мало здоровья",
                                font=("Softie Cyr", 25), anchor=W)
        self.canvas.create_text(200, 720,
                                text="Для тех, кто хочет бросить себе вызов.",
                                font=("Softie Cyr", 25), anchor=W)
        self.check = self.canvas.create_text(62, 200, text="✔", font=("Softie Cyr", 30), anchor=NW)
        for y_start in [200, 350, 500, 650]:
            self.canvas.create_rectangle(50, y_start, 100, y_start + 50, activefill="lime", width=3)

        self.tank = self.canvas.create_image(1466, 800, image=self.tankSprite)

    def mouse_touch(self, event):
        if not self.InRules:
            if 50 <= event.x <= 100:
                if event.y >= 200 and event.y <= 250:
                    self.difficult = 0
                    self.canvas.moveto(self.check, 62, 200)
                elif event.y >= 350 and event.y <= 400:
                    self.difficult = 1
                    self.canvas.moveto(self.check, 62, 350)
                elif event.y >= 500 and event.y <= 550:
                    self.difficult = 2
                    self.canvas.moveto(self.check, 62, 500)
                elif event.y >= 650 and event.y <= 700:
                    self.difficult = 3
                    self.canvas.moveto(self.check, 62, 650)

            if 1100 <= event.x <= 1500 and 232 <= event.y<=632:
                GameSettings.In_menu = False
                self.canvas.itemconfig(self.buttonDown, fill="", outline="")
                self.canvas.itemconfig(self.buttonUp, fill="yellow")
                self.canvas.itemconfig(self.textStart, text="")
                fire = self.canvas.create_oval(1220, 660, 1320, 760, fill="orange red", outline="orange red")
                for i in range(500):
                    self.canvas.move(self.buttonUp, 5, 0)
                    self.canvas.move(fire, -2, -1)
                    self.update()

                GameSettings.difficult = self.difficult
                self.destroy()

                self.configire_Game()
                self.start_game()
            if 0 <= event.x <= 400 and 770 < event.y < 870:
                GameSettings.In_menu = False
                self.canvas.delete("all")
                self.rules_menu()
        if self.InRules and event.x<305 and event.y < 305:
            self.InRules = False
            GameSettings.In_menu = True
            self.canvas.delete("all")
            self.draw_interface()



    def loop(self):
        while GameSettings.In_menu == True:

            self.update()

    def rules_menu(self):


        self.canvas.create_image(0, 0, anchor=NW, image=self.rulesImage)
        self.canvas.create_rectangle(5, 5, 305, 105, fill="red")
        self.canvas.create_text(155, 55, text="Назад", font=("Softie Cyr", 60, "bold"))
        self.canvas.create_rectangle(5, 5, 305, 105, fill="",
                                     activefill="yellow", activeoutline="red", outline="")
        self.InRules = True
        while self.InRules:
            self.update()

    def configire_Game(self):
        self.settings = SettingsMap
        if self.difficult == 0:
            self.settings.enemys = 1
            self.settings.bonuses = 0
            self.settings.bonusUp = 0
        elif self.difficult == 1:
            self.settings.enemys = 1
            self.settings.bonuses = 7
            self.settings.bonusUp = 100
            tankSettings.health = 100
        elif self.difficult == 2:
            self.settings.enemys = 1
            self.settings.bonuses = 3
            self.settings.bonusUp = 25
            tankSettings.health = 25
        elif self.difficult == 3:
            self.settings.enemys = 5
            self.settings.bonuses = 1
            self.settings.bonusUp = 10
            tankSettings.health = 10



    def start_game(self):
        GameSettings.session = True
        GameSettings.win = False
        GameSettings.endGame = False
        gameClass.loadBest(5)

        matrix = mapClass.Map(10, self.settings)

        window = windowClass.Window(12)  # tankSettings.visibleZone*2+1)

        members = []

        for m in range(1, len(matrix.enemysCords) + 1):
            members.append(Tank(m, matrix.enemysCords[m - 1], window))
        tankSettings.playerID = m + 1
        matrix.matrix[SettingsMap.playerPosition[1] + 1][ SettingsMap.playerPosition[0] + 1] = m+1

        members.append(Tank(m + 1, (SettingsMap.playerPosition[0] + 1, SettingsMap.playerPosition[1] + 1), window))
        gameClass.Game(map=matrix.matrix, bonusAdd=self.settings.bonusUp, members=members, window=window)

    def on_closing(self):
        GameSettings.work = False
        GameSettings.In_menu = False
        GameSettings.session = False




while GameSettings.work:
    s = startWindow()

