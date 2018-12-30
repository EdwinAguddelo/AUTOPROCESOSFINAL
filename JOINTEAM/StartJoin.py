from JOINTEAM.BuildDataFrames import *


class StartJoins():
    def __init__(self,path):
        self.backupFile=path.BackUpPathFile
        self.filesDefectos=path.filesDefectos
        self.filesCasosPrueba=path.filesCasosPrueba

        self.backupDataSet = backupBuild(self.backupFile)

        self.dataframesCasosPrueba = buildDtf(self.filesCasosPrueba,'Query1')
        self.dataframesDefectos = buildDtf(self.filesDefectos,'Sheet1')
        self.dataframesofDefectos = eliminateFields(self.dataframesDefectos)

    def getfileDefectos(self):
        return self.filesDefectos

    def getfilesCasosPrueba(self):
        return self.filesCasosPrueba

    def mergeCasosPrueba(self):
        dtfCasosPrueba = []
        for dtFrame in self.dataframesCasosPrueba:
            dtFrame = dtFrame.merge(self.backupDataSet,left_on='REL_USER_TEMPLATE_01',right_on='USUARIO',how='inner')
            dtFrame = dtFrame.drop(columns=['TEAM','USUARIO'])
            dtfCasosPrueba.append(dtFrame)
        return dtfCasosPrueba

    def mergeDefectos(self):
        dtfDefectos = []
        for dtFrame in self.dataframesofDefectos:
            dtFrame = dtFrame.merge(self.backupDataSet,left_on='Detected By',right_on='USUARIO',how='inner')
            dtFrame = dtFrame.drop(columns=['USUARIO'])
            dtfDefectos.append(dtFrame)
        return dtfDefectos
