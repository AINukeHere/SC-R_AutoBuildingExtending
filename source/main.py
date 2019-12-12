import os
os.system('cls')

from eudplib import * 
import TileManager
import JobManager
import unitLoop
import BuildingInfo

TileManager.init()

def onPluginStart():
    TileManager.InGameInit()
    BuildingInfo.init()
    pass
    #JobManager.CreateJob(EncodeUnit("Terran Missile Turret"))

curTestIndex = EUDVariable()
testSize = EUDVariable(16)
def beforeTriggerExec():
    global curTestIndex
    if EUDIf()(curTestIndex + testSize > 128*10):#TileManager.tileNum):
        f_simpleprint('reset')
        curTestIndex << 0
    EUDEndIf()
    TileManager.VisualizingTileDB(curTestIndex,curTestIndex+testSize)
    curTestIndex += testSize
    unitLoop.main()

def afterTriggerExec():
    DoActions([
        # eudTurbo
        SetMemory(0x6509A0, SetTo, 0),
    ])
