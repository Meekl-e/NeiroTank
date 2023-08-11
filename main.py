from window import windowClass
from SpawnScripts import mapClass
from gameScripts import gameClass
from SpawnScripts.SettingsClass import SettingsMap
from TankScripts.tankClass import Tank
from TankScripts.tankSettings import tankSettings



SIZE = 20

ENEMYS = 3

HEALTH_ENEMY= 50


BONUSES = 10
BONUS_ADD = 50

WALLS_SPAWN = 0

VISIBLE_ZONE = 3



settings = SettingsMap
settings.enemys = ENEMYS
#settings.respawnEnemys = RESPAWN_ENEMYS
settings.bonuses = BONUSES
settings.wallsSpawns = WALLS_SPAWN
settings.playerPosition = (5,5)


tankSettings.visibleZone = VISIBLE_ZONE
tankSettings.health = HEALTH_ENEMY







while True:
    gameClass.loadBest(VISIBLE_ZONE)
    matrix = mapClass.Map(SIZE, settings)
    window = windowClass.Window(SIZE+2)#tankSettings.visibleZone*2+1)
    neuralNetwok = None #NeuralNetwork()
    #neuralNetwok.learn()
    members = []
    for m in range(1, len(matrix.enemysCords) + 1):
        members.append(Tank(m, matrix.enemysCords[m - 1], window, neuralNetwok))
    members.append(Tank(-1, (settings.playerPosition[0]+1, settings.playerPosition[1]+1), window, neuralNetwok))
    g = gameClass.Game(map=matrix.matrix, bonusAdd=BONUS_ADD, members=members, window=window)










