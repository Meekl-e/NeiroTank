from window import windowClass
from SpawnScripts import mapClass
from gameScripts import gameClass
from SpawnScripts.SettingsClass import SettingsMap
from TankScripts.tankClass import Tank
from TankScripts.tankSettings import tankSettings
from gameScripts.gameSettings import GameSettings


SIZE = 10

ENEMYS = 1

HEALTH_ENEMY= 50


BONUSES = 3
BONUS_ADD = 50

WALLS_SPAWN = 0

VISIBLE_ZONE = 5



settings = SettingsMap
settings.enemys = ENEMYS
#settings.respawnEnemys = RESPAWN_ENEMYS
settings.bonuses = BONUSES
settings.wallsSpawns = WALLS_SPAWN
settings.playerPosition = (3,5)


tankSettings.visibleZone = VISIBLE_ZONE
tankSettings.health = HEALTH_ENEMY







while True:
    gameClass.loadBest(VISIBLE_ZONE)
    matrix = mapClass.Map(SIZE, settings)
    window = windowClass.Window(SIZE+2)#tankSettings.visibleZone*2+1)
    GameSettings.session = True
    GameSettings.difficult = 1
    GameSettings.In_menu = False
    members = []
    for m in range(1, len(matrix.enemysCords) + 1):
        members.append(Tank(m, matrix.enemysCords[m - 1], window))
    tankSettings.playerID = m+1
    members.append(Tank(m+1, (settings.playerPosition[0]+1, settings.playerPosition[1]+1), window))
    g = gameClass.Game(map=matrix.matrix, bonusAdd=BONUS_ADD, members=members, window=window)










