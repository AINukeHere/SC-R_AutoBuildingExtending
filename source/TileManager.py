from eudplib import *

chkt = GetChkTokenized()
MTXM = bytearray(chkt.getsection('MTXM'))
UNIT = bytearray(chkt.getsection('UNIT'))

mapsize=(128,128)
print('MTXM len : ', len(MTXM))
MTXM_STRUCT_SIZE = 2
tileNum = int(len(MTXM) / MTXM_STRUCT_SIZE)
print('tileNum : ' , tileNum)
tileDB = [0]*tileNum
tileCV5 = []
CV5_STRUCT_SIZE = 52
tileVF4 = []
VF4_STRUCT_SIZE = 32
tileSet = []

print('UNIT len : ', len(UNIT))
UNIT_STRUCT_SIZE = 36
print('unit count : ', len(UNIT)/UNIT_STRUCT_SIZE)

#tileDBforInGame = Db(tileNum)
tileDBforInGame = EUDArray(tileNum)
testRange = 1500
def InGameInit():
    for i in range(tileNum):
        tileDBforInGame[i] = tileDB[i]

# 단일인덱스 출력. 안쓸거임
# def VisualizingTileDB(idx):
#     if EUDIf()(tileDBforInGame[idx] & 0x01) == 1:
#         X = (idx%mapsize[0])*32
#         Y = (idx//mapsize[0])*32

#         DoActions([
#             SetMemory(0x58DC60, SetTo, X),
#             SetMemory(0x58DC64, SetTo, Y),
#             SetMemory(0x58DC68, SetTo, X+32),
#             SetMemory(0x58DC6C, SetTo, Y+32),
#             CreateUnit(1,"Terran Marine","Location 0", P1),
#         ])
#     EUDEndIf()

def VisualizingTileDB(start,end):
    i = EUDVariable()
    i << start
    if EUDWhile()(end > i):
        X = (i % mapsize[0])*32
        Y = (i // mapsize[1])*32
        DoActions([
            SetMemory(0x58DC60, SetTo, X),
            SetMemory(0x58DC64, SetTo, Y),
            SetMemory(0x58DC68, SetTo, X+32),
            SetMemory(0x58DC6C, SetTo, Y+32),
        ])
        if EUDIf()((tileDBforInGame[i] & 0x04) != 0):
            DoActions([
                CreateUnit(1,"Zerg Scourge","Location 0", P1),
            ])
        if EUDElseIf()(EUDSCAnd()((tileDBforInGame[i] & 0x02) != 0)(tileDBforInGame[i] & 0x01 != 0)()):
            DoActions([
                CreateUnit(1,"Gui Montag","Location 0", P1),
            ])
        if EUDElseIf()((tileDBforInGame[i] & 0x01) != 0):
            DoActions([
                CreateUnit(1,"Jim Raynor (Marine)","Location 0", P1),
            ])
        EUDEndIf()
        

        DoActions([
            KillUnit(EncodeUnit("Jim Raynor (Marine)"),P1),
            KillUnit(EncodeUnit("Gui Montag"),P1),
            KillUnit(EncodeUnit("Zerg Scourge"),P1),
        ])
        i+=1
    EUDEndWhile()

def OnNewBuilding(xmin,ymin,width,height):
    for deltaX in EUDLoopRange(width):
        for deltaY in EUDLoopRange(height):
            tileDBforInGame[(xmin+deltaX) + (ymin+deltaY)*mapsize[0]] |= 0x04
def OnDestroyBuilding(xmin,ymin,width,height):
    for deltaX in EUDLoopRange(width):
        for deltaY in EUDLoopRange(height):
            tileDBforInGame[(xmin+deltaX) + (ymin+deltaY)*mapsize[0]] &= ~0x04

def GetBuildPosition(searchStartPosX,searchStartPosY):
    return searchStartPosX,searchStartPosY
# tildDB bit info
# 0x01 : 지형이 허용이 되는가? (허용되면 1, 허용되지않으면 0)
# 0x02 : 자원필드가 있어 특정건물(커맨드센터,해처리,넥서스)을 지을 수 없는 타일인가?(자원필드범위가 있으면 1, 없으면 0)
# 0x04 : 건물이 이미 지어져있는가? (지어져있으면 1, 없으면 0)
def init():
    # CV5 파일분석
    f = open('tileset/jungle.cv5','rb')
    while True:
        obj = f.read(CV5_STRUCT_SIZE)
        if len(obj) < CV5_STRUCT_SIZE:
            #print('end of file : ' , len(obj))
            break
        for i in range(20,52,2):
            tileSet.append(int.from_bytes(obj[i:i+2],byteorder='little',signed=False))
        #print()

        tileCV5.append(obj)
    #print('tileCV5 read', len(tileCV5))

    #print('tileSet len : ', len(tileSet))

    f = open('tileset/jungle.vf4','rb')
    while True:
        obj = f.read(VF4_STRUCT_SIZE)
        if len(obj) < VF4_STRUCT_SIZE:
            #print('end of file : ' , len(obj))
            break
        tileVF4.append(obj)
    #print('tileVF4 read', len(tileVF4))

    ## MTXM으로부터 tileDB 초기화
    tempPrintCount = 10
    for i in range(0, len(MTXM), MTXM_STRUCT_SIZE):
        megaTileIndexByteArray = MTXM[i:i+2]
        megaTileIndex = int.from_bytes(megaTileIndexByteArray,byteorder='little',signed=False)
        megaTileRowIndex = int(megaTileIndex / 16)
        buildable = tileCV5[megaTileRowIndex][2] >> 4 == 0
        mapTileIndex = i >> 1
        if buildable:
            tileDB[mapTileIndex] |= 0x01
        else:
            tileDB[mapTileIndex] &= ~0x01
        # if tempPrintCount > 0:
        #     tempPrintCount-=1
        #     print(buildable)
    # 자원필드 정보초기화
    for i in range(0, len(UNIT), UNIT_STRUCT_SIZE):
        unitID = int.from_bytes(UNIT[i+8:i+10],byteorder='little',signed=False)
        if unitID == EncodeUnit("Mineral Field (Type 1)") or unitID == EncodeUnit("Mineral Field (Type 2)") or unitID == EncodeUnit("Mineral Field (Type 3)"):
            posX = int.from_bytes(UNIT[i+4:i+6],byteorder='little',signed=False)
            posY = int.from_bytes(UNIT[i+6:i+8],byteorder='little',signed=False)
            tileX = posX // 32
            tileY = posY // 32
            # 자원부분은 절대로 못지음
            tileDB[tileX-1 + tileY*mapsize[0]] &= ~0x01
            tileDB[tileX+0 + tileY*mapsize[0]] &= ~0x01
            # 자원주위 커맨드,해처리,넥서스 못지음
            for y in range(-3,3):
                for x in range(-4,4):
                    tileDB[tileX+x + (tileY+y)*mapsize[0]] |= 0x02
                    #print('[',x,',',y,']')
            # 두번째줄
            # tileDB[tileX-4 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX-3 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX-2 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX-1 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX-0 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX+1 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX+2 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX+3 + (tileY-3)*mapsize[0]] |= 0x02

        elif unitID == EncodeUnit("Vespene Geyser"):
            posX = int.from_bytes(UNIT[i+4:i+6],byteorder='little',signed=False)
            posY = int.from_bytes(UNIT[i+6:i+8],byteorder='little',signed=False)
            tileX = posX // 32
            tileY = posY // 32
            #자원부분은 절대로 못지음
            tileDB[tileX-2 + (tileY-1)*mapsize[0]] &= ~0x01
            tileDB[tileX-1 + (tileY-1)*mapsize[0]] &= ~0x01
            tileDB[tileX-0 + (tileY-1)*mapsize[0]] &= ~0x01
            tileDB[tileX+1 + (tileY-1)*mapsize[0]] &= ~0x01
            tileDB[tileX-2 + (tileY+0)*mapsize[0]] &= ~0x01
            tileDB[tileX-1 + (tileY+0)*mapsize[0]] &= ~0x01
            tileDB[tileX-0 + (tileY+0)*mapsize[0]] &= ~0x01
            tileDB[tileX+1 + (tileY+0)*mapsize[0]] &= ~0x01
            # 자원주위 커맨드,해처리,넥서스 못지음
            for y in range(-4,4):
                for x in range(-5,5):
                    tileDB[tileX+x + (tileY+y)*mapsize[0]] |= 0x02

    print('tileDB sample')
    for i in range(128,128+256+128):
        #print('[',i,']',tileDB[i])
        print(tileDB[i],end=' ')
    