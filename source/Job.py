from eudplib import *

class CJob(EUDStruct):
    _fields_ = [
        'builderEPD',
        'buildType',
        'buildPosX',
        'buildPosY',
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
        # self.__setattr__('builderEPD',builderEPD)
        # self.__setattr__('buildType',buildType)
        # self.__setattr__('buildPosX',buildPosX)
        # self.__setattr__('buildPosY',buildPosY)
        f_simpleprint(builderEPD,buildType,buildPosX,buildPosY)
    def update(self):
        if EUDIf()(self.builderEPD != 0):
            orderID = self.builderEPD + 0x4D // 4
            unitPosX_EPD = self.builderEPD + 0x28 //4
            unitPosY_EPD = self.builderEPD + 0x2A //4
            unitPosX = f_wread_epd(unitPosX_EPD, 0)
            unitPosY = f_wread_epd(unitPosY_EPD, 2)
            orderIDValue = f_wread_epd(orderID, 0x4D % 4)
            if EUDIf()(MemoryXEPD(orderID, Exactly, 0x00000300, 0x0000FF00)):
                f_simpleprint('go work!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                DoActions([
                    SetMemoryEPD(self.builderEPD+0x58 // 4, SetTo, self.buildPosX + self.buildPosY*65536),
                    SetMemoryEPD(self.builderEPD+0x98 // 4, SetTo, 14942208 + self.buildType),
                    SetMemoryEPD(self.builderEPD+0x4C // 4, SetTo, 0 + 30*256),
                ])
            EUDEndIf()
        EUDEndIf()