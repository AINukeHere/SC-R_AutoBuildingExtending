from eudplib import *

buildingInfo = EUDArray(228*2)
def init():
    global buildingInfo
    # 4x3
    buildingInfo[2*EncodeUnit('Terran Command Center') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Command Center') + 1] = 3
    buildingInfo[2*EncodeUnit('Terran Barracks') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Barracks') + 1] = 3
    buildingInfo[2*EncodeUnit('Terran Factory') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Factory') + 1] = 3
    buildingInfo[2*EncodeUnit('Terran Starport') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Starport') + 1] = 3
    buildingInfo[2*EncodeUnit('Terran Science Facility') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Science Facility') + 1] = 3
    buildingInfo[2*EncodeUnit('Terran Engineering Bay') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Engineering Bay') + 1] = 3
    # 4x2
    buildingInfo[2*EncodeUnit('Terran Refinery') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Refinery') + 1] = 2
    # 3x2
    buildingInfo[2*EncodeUnit('Terran Supply Depot') + 0] = 3
    buildingInfo[2*EncodeUnit('Terran Supply Depot') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Academy') + 0] = 3
    buildingInfo[2*EncodeUnit('Terran Academy') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Armory') + 0] = 3
    buildingInfo[2*EncodeUnit('Terran Armory') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Bunker') + 0] = 3
    buildingInfo[2*EncodeUnit('Terran Bunker') + 1] = 2
    # 2x2
    buildingInfo[2*EncodeUnit('Terran Comsat Station') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Comsat Station') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Nuclear Silo') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Nuclear Silo') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Control Tower') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Control Tower') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Covert Ops') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Covert Ops') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Physics Lab') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Physics Lab') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Machine Shop') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Machine Shop') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Missile Turret') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Missile Turret') + 1] = 2
@EUDFunc
def GetBuildSizeX(unitType):
    EUDReturn(buildingInfo[2*unitType + 0])
@EUDFunc
def GetBuildSizeY(unitType):
    EUDReturn(buildingInfo[2*unitType + 1])