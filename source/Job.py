from eudplib import *

class CJob(EUDStruct):
    _fields_ = [
        'builderEPD'
        'buildType'
    ]
    # def __init__(self, builderEPD, buildType):
    #     if isinstance(builderEPD, int):
    #         super().__init__([
    #             builderEPD,buildType
    #         ])
    #     else:
    #         super().__init__(builderEPD)
    def update(self):
        pass
    def constructor(self, builderEPD, buildType):
        f_simpleprint(builderEPD,buildType)