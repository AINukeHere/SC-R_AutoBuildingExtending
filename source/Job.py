from eudplib import *

class CJob(EUDStruct):
    _fields_ = [
        'builderEPD',
        'buildType',
        'buildPosX',
        'buildPosY',
        'isBuildStart',
    ]
    # def __init__(self, builderEPD, buildType):
    #     if isinstance(builderEPD, int):
    #         super().__init__([
    #             builderEPD,buildType
    #         ])
    #     else:
    #         super().__init__(builderEPD)
    def constructor(self, builderEPD, buildType, buildPosX, buildPosY):
        self.builderEPD = builderEPD
        self.buildType = buildType
        self.buildPosX = buildPosX
        self.buildPosY = buildPosY
        self.isBuildStart = 0
        f_simpleprint('Created Job',builderEPD,buildType,buildPosX,buildPosY,self.isBuildStart)
    @EUDMethod
    def updateJobInfo(self, builderEPD, buildType, buildPosX, buildPosY):
        self.builderEPD = builderEPD
        self.buildType = buildType
        self.buildPosX = buildPosX
        self.buildPosY = buildPosY
        self.isBuildStart = 0
        f_simpleprint('Updated Job',builderEPD,buildType,buildPosX,buildPosY,self.isBuildStart)
    @EUDMethod
    def update(self):
        if EUDIf()(self.isBuildStart == 0):
            orderID = self.builderEPD + 0x4D // 4
            unitPosX_EPD = self.builderEPD + 0x28 //4
            unitPosY_EPD = self.builderEPD + 0x2A //4
            unitPosX = f_wread_epd(unitPosX_EPD, 0)
            unitPosY = f_wread_epd(unitPosY_EPD, 2)
            orderIDValue = f_bread_epd(orderID, 0x4D % 4)
            #f_simpleprint(unitPosX,unitPosY,orderIDValue)
            # orderID가 Stop인경우
            if EUDIf()(orderIDValue == 3):
                #f_simpleprint('go work!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                DoActions([
                    SetMemoryEPD(self.builderEPD+0x58 // 4, SetTo, self.buildPosX + self.buildPosY*65536),
                    SetMemoryEPD(self.builderEPD+0x98 // 4, SetTo, 14942208 + self.buildType),
                    SetMemoryEPD(self.builderEPD+0x4C // 4, SetTo, 0 + 30*256),
                ])
            EUDEndIf()
            
            if EUDIf()(EUDSCOr()
                (orderIDValue == 33) # SCV의 orderID가 isBuilding(SCV)인 경우
                (orderIDValue == 0) # SCV의 orderID가 0인경우 (파괴된 경우)
                ()):
                f_simpleprint('Job Finished')
                self.isBuildStart = 1
            EUDEndIf()
        EUDEndIf()