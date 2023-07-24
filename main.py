from window import windowClass
from SpawnScripts import mapClass
from gameScripts import gameClass
from SpawnScripts.SettingsClass import SettingsMap
from TankScripts.tankClass import Tank
from TankScripts.tankSettings import tankSettings
SIZE = 100

ENEMYS = 100
REMOVE_HEALTH_PER_CHOICE = 1
HEALTH_ENEMY= 100
CHANCE_MUTATION = 100
VALUE_MUTAION =5

BONUSES = 9000
BONUS_ADD = 100
BONUS_UP = 0.06

WALLS_SPAWN = 0

VISIBLE_ZONE = 5

MAX_MEMBERS = 800 # int((SIZE**2-BONUSES)/1.5)
DIFFICULT_LEVEL = 50


settings = SettingsMap
settings.enemys = ENEMYS
#settings.respawnEnemys = RESPAWN_ENEMYS
settings.bonuses = BONUSES
settings.removeHealth = REMOVE_HEALTH_PER_CHOICE
settings.wallsSpawns = WALLS_SPAWN
settings.playerPosition = (1,1)
settings.maxMembers = MAX_MEMBERS
settings.bonusUp = BONUS_UP

tankSettings.visibleZone = VISIBLE_ZONE
tankSettings.health = HEALTH_ENEMY
tankSettings.chanceMutation = CHANCE_MUTATION
tankSettings.valueMutaion = VALUE_MUTAION





#window = None



while True:
    gameClass.loadBest(VISIBLE_ZONE)
    settings.bonuses = BONUSES
    settings.removeHealth = REMOVE_HEALTH_PER_CHOICE
    matrix = mapClass.Map(SIZE, settings)
    #window = windowClass.Window(len(matrix.matrix))
    #window.updateMatrix(matrix.matrix)
    window = None
    members = []
    for m in range(1,len(matrix.enemysCords)+1):
        members.append(Tank(m, matrix.enemysCords[m-1], window, mutaion=tankSettings.mutation, gens=tankSettings.matrixWeights, valueMutaion=tankSettings.valueMutaion,chanceMutation=tankSettings.chanceMutation))
    g = gameClass.Game(map =matrix.matrix, bonusAdd=BONUS_ADD, members=members, window=window)
    SettingsMap.bonusUp= SettingsMap.bonusUp+0.01
    #window.destroy()
    print("BONUSES_WAS: ", SettingsMap.bonuses)
    print("ADDING BONUS: ", SettingsMap.bonusUp-0.01)
    print("END GAME")
    print("=====================================")












