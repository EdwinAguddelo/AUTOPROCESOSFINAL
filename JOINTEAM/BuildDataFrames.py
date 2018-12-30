import pandas as pd

def backupBuild(BackUpPathFile):
    backupDataSet = pd.read_excel(BackUpPathFile)

    backupDataSet = backupDataSet[['EQUIPO','USUARIO DE RED BANCO']]
    backupDataSet = backupDataSet.rename(columns = {'USUARIO DE RED BANCO':'USUARIO'})
    backupDataSet['USUARIO'] = backupDataSet['USUARIO'].str.lower()
    backupDataSet['EQUIPO'] = backupDataSet['EQUIPO'].str.replace('ó','o')



    return backupDataSet


def  buildDtf(files,shtName):
    dataframesArray = []
    for path in files:
        data = pd.read_excel(path,sheet_name = shtName)
        dataframesArray.append(data)
    return dataframesArray

def eliminateFields(dataframesDefectos):
    arrayDefectosFiles = []
    for dtFrame in dataframesDefectos:
        dtFrame = dtFrame.loc[:,['Application','Defect ID','Automatic Defect','Business Impact','Defect Type','Detected in Cycle','Detected in Release','Detected By']]
        arrayDefectosFiles.append(dtFrame)
    return arrayDefectosFiles
