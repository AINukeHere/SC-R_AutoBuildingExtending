from eudplib import *
from Job import CJob
JOB_MAX = 50
#jobPool = ObjPool(JOB_MAX,Job)
jobs = EUDArray(JOB_MAX)
jobIndex = EUDVariable()

def init():
    pass
def CreateJob(buildType):
    global jobIndex
    jobs[jobIndex] = CJob(0, buildType)
    jobIndex += 1
    