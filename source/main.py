import os
os.system('cls')

from eudplib import * 
import TileManager
import JobManager
import unitLoop
import BuildingInfo

TileManager.init()

p1_spX = None
p1_spY = None
def onPluginStart():
    global p1_spX, p1_spY
    TileManager.InGameInit()
    BuildingInfo.init()
    JobManager.init()

    P1_startPositionX = EPD(0x58D720)
    P1_startPositionY = EPD(0x58D722)
    p1_spX = f_wread_epd(P1_startPositionX,0)
    p1_spY = f_wread_epd(P1_startPositionY,2)
    f_simpleprint("StartPosition : ", p1_spX,p1_spY)

curTestIndex = EUDVariable(128*0)
testSize = EUDVariable(16)
def beforeTriggerExec():
    global curTestIndex, p1_spX, p1_spY
    if EUDIf()(curTestIndex + testSize > 128*125):#TileManager.tileNum):
        #f_simpleprint('reset')
        curTestIndex << 128*0
    EUDEndIf()
    TileManager.VisualizingTileDB(curTestIndex,curTestIndex+testSize)
    curTestIndex += testSize

    # if EUDIf()(f_bread(0x596A18 + 32) == 1):
    #     f_simpleprint('Attempt to create a job')
    #     JobManager.CreateJob(EncodeUnit("Terran Supply Depot"), p1_spX, p1_spY)
    # EUDEndIf()
    #JobManager.CreateJob(EncodeUnit("Terran Refinery"), 3808,96)#p1_spX, p1_spY)
    #JobManager.CreateJob(EncodeUnit("Terran Barracks"), 3808,96)#p1_spX, p1_spY)
    #JobManager.CreateJob(EncodeUnit("Terran Missile Turret"), p1_spX, p1_spY)
    #DoActions(MoveLocation(EncodeLocation("Anywhere"), EncodeUnit("Tom Kazansky"), P1, EncodeLocation("Location 1")))
    DoActions(MoveLocation(EncodeLocation("Location 1"), EncodeUnit("Tom Kazansky"), P1, EncodeLocation("Anywhere")))
    loc1PosX = ( f_dwread_epd(EPD(0x58DC68)+5) + f_dwread_epd(EPD(0x58DC60)+5) ) // 2
    loc1PosY = ( f_dwread_epd(EPD(0x58DC6C)+5) + f_dwread_epd(EPD(0x58DC64)+5) ) // 2
    #f_simpleprint(loc1PosX,loc1PosY)
    if EUDIf()(Command(P1,AtLeast,1,EncodeUnit("Terran Marine"))):
        DoActions(RemoveUnit(EncodeUnit("Terran Marine"),P1))
        f_simpleprint('서플을 지읍시다.')
        JobManager.CreateJob(EncodeUnit("Terran Supply Depot"), loc1PosX, loc1PosY)
    EUDEndIf()
    if EUDIf()(Command(P1,AtLeast,1,EncodeUnit("Terran Firebat"))):
        DoActions(RemoveUnit(EncodeUnit("Terran Firebat"),P1))
        f_simpleprint('커맨드를 지읍시다.')
        JobManager.CreateJob(EncodeUnit("Terran Command Center"), loc1PosX, loc1PosY)
    EUDEndIf()
    if EUDIf()(Command(P1,AtLeast,1,EncodeUnit("Terran Medic"))):
        DoActions(RemoveUnit(EncodeUnit("Terran Medic"),P1))
        f_simpleprint('터렛을 지읍시다.')
        JobManager.CreateJob(EncodeUnit("Terran Missile Turret"), loc1PosX, loc1PosY)
    EUDEndIf()
    if EUDIf()(Command(P1,AtLeast,1,EncodeUnit("Terran Ghost"))):
        DoActions(RemoveUnit(EncodeUnit("Terran Ghost"),P1))
        f_simpleprint('벙커를 지읍시다.')
        JobManager.CreateJob(EncodeUnit("Terran Bunker"), loc1PosX, loc1PosY)
    EUDEndIf()
    unitLoop.main()
    JobManager.Update()

def afterTriggerExec():
    DoActions([
        # eudTurbo
        SetMemory(0x6509A0, SetTo, 0),
    ])
