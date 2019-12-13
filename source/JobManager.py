from eudplib import *
import TileManager
from Job import CJob
JOB_MAX = 50
#jobPool = ObjPool(JOB_MAX,CJob)
jobs = EUDArray(JOB_MAX)
jobIndex = EUDVariable()

def init():
    pass
def CreateJob(buildType, searchStartPosX, searchStartPosY):
    global jobIndex
    buildPosX,buildPosY = TileManager.GetBuildPosition(searchStartPosX,searchStartPosY)
    buildTileX = buildPosX // 32
    buildTileY = buildPosY // 32
    jobs[jobIndex] = CJob(EPD(0x59CCA8), buildType, buildPosX, buildPosY)
    jobIndex += 1
def Update():
    for i in EUDLoopRange(0,JOB_MAX):
        if EUDIf()(jobs[i] != 0):
            CJob.cast(jobs[i]).update()
        EUDEndIf()
