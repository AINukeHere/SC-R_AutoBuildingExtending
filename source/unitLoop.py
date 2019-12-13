from eudplib import *
import BuildingInfo
from TileManager import OnNewBuilding, OnDestroyBuilding

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

            f_simpleprint('New Ground Building')
            unitPosX_EPD = epd + 0x28 //4
            unitPosY_EPD = epd + 0x2A //4
            unitPosX = f_wread_epd(unitPosX_EPD, 0)
            unitPosY = f_wread_epd(unitPosY_EPD, 2)
            buildSizeX = BuildingInfo.GetBuildSizeX(unitType)
            buildSizeY = BuildingInfo.GetBuildSizeY(unitType)
            buildingXmin = (unitPosX // 32) - buildSizeX // 2
            buildingYmin = (unitPosY // 32) - buildSizeY // 2
            OnNewBuilding(buildingXmin,buildingYmin,buildSizeX,buildSizeY)
                    

        EUDEndIf()
        #f_simpleprint('newUnit')

    for ptr, epd in EUDLoopUnit2():
        orderID = epd + 0x4D // 4
        csprite = epd + 0x0C // 4
        statusFlags = epd + 0xDC //4
        
        # 유닛이 파괴되었을 경우
        if EUDIf()(EUDSCAnd()
        (MemoryXEPD(orderID, Exactly, 0, 0x0000FF00))
        (MemoryXEPD(statusFlags, AtLeast, 1, 2))()
        ):
                f_simpleprint('Destory Ground Building')
                unitPosX_EPD = epd + 0x28 //4
                unitPosY_EPD = epd + 0x2A //4
                unitPosX = f_wread_epd(unitPosX_EPD, 0)
                unitPosY = f_wread_epd(unitPosY_EPD, 2)
                buildSizeX = BuildingInfo.GetBuildSizeX(unitType)
                buildSizeY = BuildingInfo.GetBuildSizeY(unitType)
                buildingXmin = (unitPosX // 32) - buildSizeX // 2
                buildingYmin = (unitPosY // 32) - buildSizeY // 2
                OnDestroyBuilding(buildingXmin,buildingYmin,buildSizeX,buildSizeY)
        EUDEndIf()

        # Test code
        unitTypeEPD = epd + 0x64 // 4
        playerID = epd + 0x4C // 4
        if EUDIf()(EUDSCAnd()
        (MemoryEPD(unitTypeEPD, Exactly, EncodeUnit('Terran SCV')))
        (MemoryXEPD(playerID, Exactly, 0, 0xFF))
        ()
        ):
            orderID = epd + 0x4D // 4
            unitPosX_EPD = epd + 0x28 //4
            unitPosY_EPD = epd + 0x2A //4
            unitPosX = f_wread_epd(unitPosX_EPD, 0)
            unitPosY = f_wread_epd(unitPosY_EPD, 2)
            orderIDValue = f_wread_epd(orderID, 0x4D % 4)
            #f_simpleprint(unitPosX,unitPosY,orderIDValue)
            # if EUDIf()(MemoryXEPD(orderID, Exactly, 0x00000300, 0x0000FF00)):
            #     #f_simpleprint('go work!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            #     DoActions([
            #         # SetMemoryEPD(epd+0x58 // 4, SetTo, 109*32 + 7*32*65536),
            #         # SetMemoryEPD(epd+0x98 // 4, SetTo, 14942208 + EncodeUnit('Terran Supply Depot')),
            #         # SetMemoryEPD(epd+0x4C // 4, SetTo, 0 + 30*256),
            #         # SetMemory(ptr+0x58, SetTo, 109*32 + 7*32*65536),
            #         # SetMemory(ptr+0x98, SetTo, 14942208 + EncodeUnit('Terran Supply Depot')),
            #         # SetMemory(ptr+0x4C, SetTo, 0 + 30*256),
            #     ])
            # EUDEndIf()
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