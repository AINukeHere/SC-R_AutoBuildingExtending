from eudplib import *
import TileManager
from Job import CJob
JOB_MAX = 50
#jobPool = ObjPool(JOB_MAX,CJob)
jobs = EUDArray(JOB_MAX)
jobIndex = EUDVariable()

def init():
    for i in EUDLoopRange(0,JOB_MAX):
        jobs[i] = CJob.alloc(0,0,0,0)
        CJob.cast(jobs[i]).isBuildStart = 1
@EUDFunc
def CreateJob(buildType, searchStartPosX, searchStartPosY):
    global jobIndex
    buildPosX,buildPosY = TileManager.GetBuildPosition(buildType, searchStartPosX, searchStartPosY, 10)
    if EUDIf()(EUDSCOr()
    (buildPosX == -1)
    (buildPosY == -1)
    ()):
        EUDReturn()
    EUDEndIf()
    for i in EUDLoopRange(0,JOB_MAX):
        if EUDIf()(CJob.cast(jobs[i]).isBuildStart != 0):
            f_simpleprint('find empty job index : ', i)
            CJob.cast(jobs[i]).updateJobInfo(EPD(0x59CCA8), buildType, buildPosX, buildPosY)
            EUDReturn()
        EUDEndIf()
    f_simpleprint('cannot found empty job')
def Update():
    for i in EUDLoopRange(0,JOB_MAX):
        CJob.cast(jobs[i]).update()
