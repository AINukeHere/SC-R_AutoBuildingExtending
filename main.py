from eudplib import * 
import TileManager

def onPluginStart():
    TileManager.init()
    pass

def beforeTriggerExec():
    pass

def afterTriggerExec():
    DoActions([
        # eudTurbo
        SetMemory(0x6509A0, SetTo, 0),
    ])
