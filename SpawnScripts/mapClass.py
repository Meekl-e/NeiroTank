import random as rnd
from copy import deepcopy

# -4 - бонус
# -3 - враг
# -2 - стена
# -1 - нет прохода
# 0 - спавн




class Map():
    def __init__(self, size, settings):
          self.settings = settings
          self.size = size
          self.matrix = [([1]*size).copy() for i in range(size)]
          self.enemysCords = []
          self.matrix[settings.playerPosition[1]][settings.playerPosition[0]] = 0
          self.enemysCords.append(settings.playerPosition)
          self.createWalls()
          self.spawnEnemys()
          self.spawnBonus()
          self.convertMatrix()

          self.convertPlayerEnemys()




    def checkPath(self, matrix):
          matrix = deepcopy(matrix)
          for y in range(self.size):
                for x in range(self.size):
                      if matrix[y][x] >0:
                            matrix[y][x] = -1

          for pathNum in range(int(self.size**2/2)):
                for y in range(self.size):
                     for x in range(self.size):
                           if matrix[y][x] == pathNum:
                                 if x != self.size-1 and matrix[y][x+1] == -1:
                                       matrix[y][x+1] = pathNum+1
                                 if x!= 0 and matrix[y][x-1] == -1:
                                       matrix[y][x-1] = pathNum+1
                                 if y != self.size-1 and matrix[y+1][x] == -1:
                                       matrix[y+1][x] = pathNum+1
                                 if y != 0 and matrix[y-1][x] == -1:
                                       matrix[y-1][x] = pathNum+1
          return matrix

    def createWalls(self):
          for y in range(self.size):
                for x in range(self.size):
                      if self.matrix[y][x] > 0 and rnd.sample([True,False], counts=[self.settings.wallsSpawns, 100-self.settings.wallsSpawns], k=1)[0] == True:
                            newMatrix = deepcopy(self.matrix)
                            newMatrix[y][x] = -2
                            newMatrix = self.checkPath(newMatrix)
                            for line in newMatrix:
                                  if -1 in line:
                                        break
                            else:
                                  self.matrix = newMatrix
    def spawnEnemys(self):
          for e in range(self.settings.enemys-1):
                x = rnd.randint(0,self.size-1)
                y =rnd.randint(0,self.size-1)
                while self.matrix[y][x] <=0 or self.checkForPlayer(x,y)==True:
                      x = rnd.randint(0, self.size - 1)
                      y = rnd.randint(0, self.size - 1)
                self.enemysCords.append((x,y))
                self.matrix[y][x] = -3
    def spawnBonus(self):
          for e in range(self.settings.bonuses):
                x = rnd.randint(0,self.size-1)
                y =rnd.randint(0,self.size-1)
                while self.matrix[y][x] <=0:
                      x = rnd.randint(0, self.size - 1)
                      y = rnd.randint(0, self.size - 1)
                self.matrix[y][x] = -4


    def convertMatrix(self):
         for y in range(self.size):
               for x in range(self.size):
                     if self.matrix[y][x] >0:
                           self.matrix[y][x] = 0
                     elif self.matrix[y][x] == 0:
                           self.matrix[y][x] = "P"
                     elif self.matrix[y][x] == -2:
                           self.matrix[y][x] = "W"
                     elif self.matrix[y][x] == -3:
                           self.matrix[y][x] = "E"
                     elif self.matrix[y][x] == -4:
                           self.matrix[y][x] = "B"


    def convertPlayerEnemys(self):
          id = 1
          for x,y in self.enemysCords:
                if self.matrix[y][x] == "P":
                      self.matrix[y][x] = id
                      id+=1
                elif self.matrix[y][x] == "E":
                      self.matrix[y][x] = id
                      id+=1
          self.matrix.insert(0, ["W"] * self.size)
          self.matrix.append(["W"] * self.size)
          for line in range(len(self.matrix)):
                self.matrix[line].append("W")
                self.matrix[line].insert(0, "W")
          self.enemysCords = list(map(lambda x:(x[0]+1,x[1]+1), self.enemysCords))
    def checkForPlayer(self, x,y):
          for pos in self.enemysCords:
                if pos[0]-3 < x < pos[0]+3 and pos[1]-3 < y < pos[1]+3:
                      return True
          return False





