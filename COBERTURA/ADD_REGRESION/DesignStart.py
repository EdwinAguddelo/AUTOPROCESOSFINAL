from ADD_REGRESION.readExcel import *


class DesignStart():
    def __init__(self,path):
        self.regresion=path.regresionPathFile
        self.soporte=path.soportePathFile

        self.regresionDT = buildDtfS(self.regresion)
        self.soporteDT = buildDtf(self.soporte)

    def getfileRegresion(self):
        return self.regresionDT

    def getfilesSoporteDT(self):
        return self.soporteDT

    def getSoporteRute(self):
        return self.soporte

    def getRegresionRute():
        return self.regresion
