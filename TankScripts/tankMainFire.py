from sklearn.neural_network import MLPClassifier


def loadData():
    f = open("TankScripts/dataFire/dataX.txt", "r")
    dataX = list(map(lambda x: map(int, x.split()), f.readlines()))
    f.close()
    f = open("TankScripts/dataFire/dataY.txt", "r")
    dataY = list(map(lambda x: map(int, x.split()), f.readlines()))
    f.close()
    return dataX,dataY


def addToFile(x,y):
    f = open("TankScripts/dataFire/dataX.txt", "r")
    if len(f.readlines()) > 100000:
        f.close()
        return
    f.close()
    f = open("TankScripts/dataFire/dataX.txt", "a")
    for s in x:
        f.write(str(s) + " ")
    f.write("\n")
    f.close()
    f = open("TankScripts/dataFire/dataY.txt", "a")
    for s in y:
        f.write(str(s) + " ")
    f.write("\n")
    f.close()





class CheckTank:
    def __init__(self, tankMap):
        self.tankMap = [i for b in tankMap for i in b]
        xTank = int(len(tankMap) / 2) + 1
        yTank = int(len(tankMap) / 2) + 1
        minDist = (9999, (-1, -1), -1)
        for y in range(len(tankMap)):
            for x in range(len(tankMap)):
                if x == xTank and y == yTank:
                    continue
                if type(tankMap[y][x])==type(int) and tankMap[y][x] > 0:
                    dist = abs(y - yTank) + abs(x - xTank)
                    if dist < minDist[0]:
                        minDist = (dist, (x, y), tankMap[y][x])
        self.minCords = minDist[1]
        self.minTank = minDist[2]
    def saveChoice(self, tankMap):
        dataY = (-1,-1)
        for y in range(len(tankMap)):
            for x in range(len(tankMap)):
                if tankMap[y][x] == self.minTank:
                    dataY = (x,y)


        addToFile(self.tankMap, dataY)



class NeuralNetwork(MLPClassifier):
    def __init__(self):
        super().__init__(random_state=1)

    def learn(self):
        dataX, dataY = loadData()
        super().fit(dataX, dataY)

    def predict(self, x):
        x = [i for b in x for i in b]
        return super().predict([x])








