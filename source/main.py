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
    #f_simpleprint(f_dwread_epd(EPD(0x58D720)))
    P1_startPositionX = EPD(0x58D720)
    P1_startPositionY = EPD(0x58D722)
    p1_spX = f_wread_epd(P1_startPositionX,0)
    p1_spY = f_wread_epd(P1_startPositionY,2)
    f_simpleprint("StartPosition : ", p1_spX,p1_spY)
    JobManager.CreateJob(EncodeUnit("Terran Supply Depot"), p1_spX,p1_spY)

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
    JobManager.Update()

def afterTriggerExec():
    DoActions([
        # eudTurbo
        SetMemory(0x6509A0, SetTo, 0),
    ])
