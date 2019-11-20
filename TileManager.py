from eudplib import *

chkt = GetChkTokenized()
MTXM = bytearray(chkt.getsection('MTXM'))

tileDB = EUDArray(0x1000)
def init():
    DoActions([
        CreateUnit(1,"Terran Marine","Location 0",P1),
    ])
    f_simpleprint("AutoBuildingRestore Initialize")
    for i in range(1, 64, 2):
        print(MTXM[i],end=' ')
        if (MTXM[i] & 8) == 0:
            tileIndex = i >> 1
            #print("i = " , tileIndex)
            tileDB[tileIndex] = 0
            X = i%64*32
            Y = int(i/64)*32
            #print(X,Y)

            DoActions([
                SetMemory(0x58DC60, SetTo, X),
                SetMemory(0x58DC64, SetTo, Y),
                SetMemory(0x58DC68, SetTo, X),
                SetMemory(0x58DC6C, SetTo, Y),
                CreateUnit(1,"Terran Marine","Location 0", P1),
            ])
        else:
            tileDB[i << 1] = -1
    f_simpleprint(X,Y)
    
    