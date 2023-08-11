import random

from sklearn.neural_network import MLPClassifier


def loadData():
    f = open("TankScripts/dataFire/dataX.txt", "r")
    dataX = list(map(lambda x: map(int, x.split()), f.readlines()))
    f.close()
    f = open("TankScripts/dataFire/dataY.txt", "r")
    dataY = list(map(lambda x: str(x).removesuffix("\n"), f.readlines()))
    f.close()
    return dataX,dataY


def addToFile(x,y):

    f = open("TankScripts/dataFire/dataX.txt", "a")
    for s in x:
        f.write(str(s) + " ")

    f.write("\n")
    f.close()
    f = open("TankScripts/dataFire/dataY.txt", "a")
    f.write(f"{y}\n")
    f.close()





class CheckTank:
    def __init__(self, tankMap):
        self.tankMap = [i for b in tankMap for i in b]

        xTank = int(len(tankMap) / 2) + 1
        yTank = int(len(tankMap) / 2) + 1
        self.variants = []
        for x in range(xTank-1,xTank+2):
            for y in range(len(tankMap)):
                if xTank==x and yTank==y:
                    continue
                if type(tankMap[y][x]) == type(int) and (tankMap[y][x]>0 or tankMap[y][x]==-1):
                    if y < yTank:
                        self.variants.append((x,y, "up"))
                    else:
                        self.variants.append((x, y, "down"))
        for y in range(yTank-1,yTank+2):
            for x in range(len(tankMap)):
                if xTank==x and yTank==y:
                    continue
                if type(tankMap[y][x]) == type(int) and (tankMap[y][x]>0 or tankMap[y][x]==-1):
                    if x < xTank:
                        self.variants.append((x,y, "left"))
                    else:
                        self.variants.append((x, y, "right"))
        if len(self.variants) ==1:
            self.fireChoice = self.variants[0][2]
        else:
            self.fireChoice = "None"



    def saveChoice(self, tankMap):
        if len(self.variants) > 1:
            for fire in self.variants:
                if tankMap[fire[1]][fire[0]] > 0 or tankMap[fire[1]][fire[0]]==-1:
                    self.fireChoice = fire[2]
                    print("break")
                    break
            else:
                print("else")
                self.fireChoice = random.choice(self.variants)[2]
            print("====")


        addToFile(self.tankMap, self.fireChoice)




class NeuralNetwork(MLPClassifier):
    def __init__(self):
        super().__init__(random_state=1)

    def learn(self):
        dataX, dataY = loadData()
        super().fit(dataX, dataY)

    def predict(self, x):
        x = [i for b in x for i in b]
        return super().predict([x])








