from eudplib import *
import BuildingInfo

newCUnit = EUDArray(1700 * 336)
epd2newCUnit = EPD(newCUnit) - EPD(0x59CCA8)

def main():
    for ptr,epd in LoopNewUnit():
        statusFlags = epd + 0xDC //4
        unitTypeEPD = epd + 0x64 // 4
        unitType = -1
        if EUDIf()(MemoryXEPD(statusFlags, AtLeast, 1, 2)):
            unitType = f_dwread_epd(unitTypeEPD)

            # 광물지대도 인식되어버리므로 예외처리
            EUDContinueIf(EUDSCOr()
            (unitType == EncodeUnit('Mineral Field (Type 1)'))
            (unitType == EncodeUnit('Mineral Field (Type 2)'))
            (unitType == EncodeUnit('Mineral Field (Type 3)'))
            (unitType == EncodeUnit('Vespene Geyser'))
            ())

            unitPosX_EPD = epd + 0x28
            unitPosY_EPD = epd + 0x2A
            unitPosX = f_wread_epd(unitPosX_EPD,0)
            unitPosY = f_wread_epd(unitPosY_EPD,3)

            f_simpleprint('groundedBuilding')
            f_simpleprint(unitType, unitPosX, unitPosY, BuildingInfo.GetBuildSizeX(unitType), BuildingInfo.GetBuildSizeY(unitType))
            buildSizeX = BuildingInfo.GetBuildSizeX(unitType)
        EUDEndIf()
        #f_simpleprint('newUnit')

    for ptr, epd in EUDLoopUnit2():
        orderID = epd + 0x4D // 4
        csprite = epd + 0x0C // 4
        statusFlags = epd + 0xDC //4
        
        # 유닛이 파괴되었을 경우
        # if EUDIf()(EUDSCAnd()(MemoryEPD(csprite, AtLeast, 1))(MemoryXEPD(orderID, Exactly, 0, 0x0000FF00))()):
        # f_simpleprint('DeadCheck')
        if EUDIf()(MemoryXEPD(orderID, Exactly, 0, 0x0000FF00)):
            if EUDIf()(MemoryXEPD(statusFlags, AtLeast, 1, 2)):
                f_simpleprint('Dead')
            EUDEndIf()
        EUDEndIf()


def LoopNewUnit(allowance=2):
    firstUnitPtr = EPD(0x628430)
    EUDCreateBlock("newunitloop", "newlo")
    tos0 = EUDLightVariable()
    tos0 << 0

    ptr, epd = f_cunitepdread_epd(firstUnitPtr)
    if EUDWhile()(ptr >= 1):
        tos1 = f_bread_epd(epd + 0xA5 // 4, 1)
        global epd2newCUnit
        tos2 = epd + epd2newCUnit
        if EUDIfNot()(MemoryEPD(tos2, Exactly, tos1)):
            DoActions(SetMemoryEPD(tos2, SetTo, tos1))
            yield ptr, epd
        if EUDElse()():
            DoActions(tos0.AddNumber(1))
            EUDBreakIf(tos0.AtLeast(allowance))
        EUDEndIf()
        EUDSetContinuePoint()
        f_cunitepdread_epd(epd + 1, ret=[ptr, epd])
    EUDEndWhile()

    EUDPopBlock("newunitloop")