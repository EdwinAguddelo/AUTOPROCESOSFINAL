import os


class setupPaths:
    def __init__(self,resourcesPath):
        self.resourcesPath = resourcesPath

        self.soporteFile = "consolidado.xlsx"
        self.regresionFile = "Regresion.xlsm"

        self.soportePathFile = os.path.join(self.resourcesPath,self.soporteFile)
        self.regresionPathFile = os.path.join(self.resourcesPath,self.regresionFile)
