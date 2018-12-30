import os

class setupPaths:
    def __init__(self,resourcesPath):
        self.resourcesPath = resourcesPath

        self.DefectosPath = "QC12P/DEFECTOS/"
        self.CasosPruebaPath = "QC12P/"
        self.BackUpPath = "BKUP/backup.xls"

        self.DefectosPathFolder = os.path.join(self.resourcesPath,self.DefectosPath)
        self.CasosPruebaPathFolder = os.path.join(self.resourcesPath,self.CasosPruebaPath)
        self.BackUpPathFile = os.path.join(self.resourcesPath, self.BackUpPath)

        self.filesDefectos = []
        self.filesCasosPrueba = []

        for file in os.listdir(self.DefectosPathFolder):
            if file.endswith('.xlsx'):
                if os.path.join(self.DefectosPathFolder,file) not in self.filesDefectos:
                   self.filesDefectos.append(os.path.join(self.DefectosPathFolder,file))

        for file in os.listdir(self.CasosPruebaPathFolder):
            if file.endswith('.xls'):
                if os.path.join(self.CasosPruebaPathFolder,file) not in self.filesCasosPrueba:
                    self.filesCasosPrueba.append(os.path.join(self.CasosPruebaPathFolder,file))
