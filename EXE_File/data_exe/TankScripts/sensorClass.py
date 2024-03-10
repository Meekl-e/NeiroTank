
import random as rnd


class Sensor:
    def __init__(self, r=0, l=0, u=0, d=0, type="" ):
        self.right = r
        self.left = l
        self.up = u
        self.down = d
        self.type = type
    def __repr__(self):
        return f"[{self.right}-r,{self.left}-l,{self.up}-u,{self.down}-d]"
    def __str__(self):
        return f"{self.right} {self.left} {self.up} {self.down}"
    def __getitem__(self, key):
        return [self.right,self.left,self.up,self.down][key]
    def __setitem__(self, key, value):
        if key == 0:
            self.right = value
        elif key == 1:
            self.left = value
        elif key == 2:
            self.up = value
        elif key == 3:
            self.down = value


class Box:
    def __init__(self, random=0):
        if random != 0:

            self.wall = Sensor(*map(lambda x:rnd.randint(-random,random),range(4) ), type="wall")
            self.bonus = Sensor(*map(lambda x:rnd.randint(-random,random),range(4) ),type="bonus")
            self.enemy = Sensor(*map(lambda x:rnd.randint(-random,random),range(4) ),type="enemy")
        else:
            self.wall = Sensor(type="wall")
            self.bonus = Sensor(type="bonus")
            self.enemy = Sensor(type="enemy")
    def getSensor(self, object):
        if object == "W":
            return self.wall
        elif object == "B":
            return self.bonus

        elif object <= 0:
            return Sensor(0,0,0,0)
        else:
            return self.enemy
    def getSensorOfType(self, type):
        if type == "bonus":
            return self.bonus
        elif type=="enemy":
            return self.enemy
        else:
            return self.wall
    def __str__(self):
        return f"{self.wall} {self.enemy} {self.bonus}"
    def __repr__(self):
        return f"[Датчик стены: {self.wall}. Датчик врага: {self.enemy}. Датчик бонуса: {self.bonus}]"
    def __getitem__(self, key):
        return [self.wall,self.enemy,self.bonus][key]
    def __len__(self):
        return 3