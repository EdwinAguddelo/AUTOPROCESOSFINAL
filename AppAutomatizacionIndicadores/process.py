import pandas as pd
import os
#from pathFiles import defectosFiles,casosPruebaFiles,transformacionFilePath,soporteFilePath
from cleaners import *
from utils import getAppsToRows,getNextSprintNumber,getNextSprintNumberUpdate
from rowModel import TransformacionRow,rowFeeder
from folderFilesToDataFrame import *
from dataWrangling import defectosDataWrangling,casosPruebaDataWrangling

global defectosFiles,casosPruebaFiles,transformacionFilePath,soporteFilePath

def pathConstructor(paths):
    global defectosFiles,casosPruebaFiles,transformacionFilePath,soporteFilePath,resourcesFiles,pittsFilePath,pittsDataSet
    defectosFiles=paths.defectosFiles
    casosPruebaFiles=paths.casosPruebaFiles
    transformacionFilePath=paths.transformacionFilePath
    soporteFilePath=paths.soporteFilePath
    resourcesFiles = paths.resourcesPath
    pittsFilePath = paths.pittsFilePath
    pittsDataSet = pd.read_excel(pittsFilePath)
def process(Direccion,baseDataFrame,sprintNumber):


    DataFrameToAppend=baseDataFrame.drop(baseDataFrame.index, inplace=False)
    AppendedDataFrame = baseDataFrame.append(DataFrameToAppend, ignore_index=True)
    defectosDataFrames=folderPathToDataFrames(defectosFiles)
    casosPruebasDataFrames=folderPathToDataFrames(casosPruebaFiles)

    wraggledDefectosDatasets,wraggledCasosPruebasDatasets,FileNames=getWraggledDataFrames(
        defectosDataFrames,casosPruebasDataFrames,Direccion,sprintNumber)

    rowToAggregate=getRowsToAggregate(wraggledDefectosDatasets,wraggledCasosPruebasDatasets,sprintNumber,FileNames)
    #updatedDataFrameToExcel(rowToAggregate,AppendedDataFrame,baseDataFrame,'consolidado{}.xlsx'.format(Direccion))
    if Direccion == 'Transformacion':
        datasetDireccion = updatedDataFrameToExcel(rowToAggregate,AppendedDataFrame,baseDataFrame,transformacionFilePath)
    elif Direccion == 'Soporte':
        datasetDireccion = updatedDataFrameToExcelSoporte(rowToAggregate,AppendedDataFrame,baseDataFrame,soporteFilePath)

    return datasetDireccion


def startProcessSoporte():
    Direccion='Soporte'
    baseDataFrame=pd.read_excel(soporteFilePath)
    sprintNumber=getNextSprintNumber(baseDataFrame)
    soporteDataset = process(Direccion,baseDataFrame,sprintNumber)
    soporteDataset['Area']='Soporte'
    return soporteDataset

def startProcessTransformacion():
    Direccion='Transformacion'
    baseDataFrame=pd.read_excel(transformacionFilePath)
    sprintNumber=getNextSprintNumber(baseDataFrame)
    transformacionDataset = process(Direccion,baseDataFrame,sprintNumber)
    transformacionDataset['Area']='Transformacion'
    return transformacionDataset

def processFinal():
    transformacionDataset = startProcessTransformacion()
    soporteDataset = startProcessSoporte()
    sprintNumberSoporte=getNextSprintNumberUpdate(soporteDataset)
    JoinDataSetFinals(transformacionDataset,soporteDataset,sprintNumberSoporte)



def getWraggledDataFrames(defectosDataFrames,casosPruebasDataFrames,Direccion,sprintNumber):

    wraggledDefectosDatasets=[]
    wraggledCasosPruebasDatasets=[]
    FileNames=[]

    for file in range(len(defectosDataFrames)):

        FileNames.append(defectosFiles[file])

        defectosDataFrame=defectosDataFrames[file]
        defectosDataFrame=defectosDataWrangling(defectosDataFrame,Direccion,sprintNumber)

        casosPruebasDataFrame=casosPruebasDataFrames[file]
        casosPruebasDataFrame=casosPruebaDataWrangling(casosPruebasDataFrame,Direccion,sprintNumber)

        wraggledDefectosDatasets.append(defectosDataFrame)
        wraggledCasosPruebasDatasets.append(casosPruebasDataFrame)

    return wraggledDefectosDatasets,wraggledCasosPruebasDatasets,FileNames

def getRowsToAggregate(wraggledDefectosDatasets,wraggledCasosPruebasDatasets,sprintNumber,FileNames):
    rowToAggregate=[]
    for index,wraggledDefectosDatasets in enumerate(wraggledDefectosDatasets):
        total=getAppsToRows(wraggledCasosPruebasDatasets[index],wraggledDefectosDatasets)

        for releaseName in total:

            feed = rowFeeder(releaseName,wraggledDefectosDatasets,wraggledCasosPruebasDatasets[index])

            rowToAggregate.append(
                TransformacionRow(
                    releaseName,sprintNumber,feed,FileNames[index]
                    ).getRow()
                )
    return rowToAggregate

def updatedDataFrameToExcel(rowToAggregate,AppendedDataFrame,baseDataFrame,excelFileName):
    for i,row in enumerate(rowToAggregate):
        DataFrameToAppend=baseDataFrame.drop(baseDataFrame.index, inplace=False)
        DataFrameToAppend.loc[i, :] = row
        AppendedDataFrame = AppendedDataFrame.append(DataFrameToAppend, ignore_index=True)


    AppendedDataFrame=AppendedDataFrame.sort_values(by=['SPRINT'],ascending=False)
    AppendedDataFrame=AppendedDataFrame.reset_index()
    AppendedDataFrame=AppendedDataFrame.drop('index',axis=1)
    AppendedDataFrame.to_excel(excelFileName,index=False)

    return AppendedDataFrame

def updatedDataFrameToExcelSoporte(rowToAggregate,AppendedDataFrame,baseDataFrame,excelFileName):
    for i,row in enumerate(rowToAggregate):
        DataFrameToAppend=baseDataFrame.drop(baseDataFrame.index, inplace=False)
        DataFrameToAppend.loc[i, :] = row
        AppendedDataFrame = AppendedDataFrame.append(DataFrameToAppend, ignore_index=True)


    AppendedDataFrame=AppendedDataFrame.sort_values(by=['SPRINT'],ascending=False)
    AppendedDataFrame=AppendedDataFrame.reset_index()
    AppendedDataFrame=AppendedDataFrame.drop('index',axis=1)

    #pittsDataSet=pd.read_excel(pittsFilePath)
    AppendedDataFrame = AppendedDataFrame.merge(pittsDataSet,left_on='PITTs',right_on='Subdominio',how='inner')
    AppendedDataFrame['PITTs_x']=AppendedDataFrame['PITTs_y'].tolist()
    AppendedDataFrame = AppendedDataFrame.drop(columns=['PITTs_y','Subdominio'])
    AppendedDataFrame = AppendedDataFrame.sort_values(by=['SPRINT'],ascending=False,)
    AppendedDataFrame = AppendedDataFrame.rename(columns={'PITTs_x':'PITTs'})

    AppendedDataFrame.to_excel(excelFileName,index=False)

    return AppendedDataFrame

def cleanColumns(dataFrameConsolidado):
    dataFrameConsolidado = dataFrameConsolidado.fillna(0)
    dataFrameConsolidado['PITTs'] = dataFrameConsolidado['PITTs'].str.upper()
    dataFrameConsolidado['Aplicación '] = dataFrameConsolidado['Aplicación '].str.upper()
    return dataFrameConsolidado

def addPittsTransformacion(dataFrameConsolidado,sprint):
    consolidado = cleanColumns(dataFrameConsolidado)
    dataFrameFiltredByTransformacion = consolidado[consolidado['Area'] == 'Transformacion']
    dataFrameFiltredByTransformacion = dataFrameFiltredByTransformacion[dataFrameFiltredByTransformacion['SPRINT'] == sprint]
    dataTransformacion = dataFrameFiltredByTransformacion.merge(pittsDataSet,left_on = 'PITTs',right_on = 'Subdominio',how = 'inner')
    dataTransformacion['PITTs_x'] = dataTransformacion['PITTs_y'].tolist()
    dataTransformacion = dataTransformacion.drop(columns = ['PITTs_y','Subdominio'])
    dataTransformacion = dataTransformacion.sort_values(by = ['SPRINT'],ascending = False)
    dataTransformacion = dataTransformacion.rename(columns = {'PITTs_x':'PITTs'})
    return dataTransformacion

def separateApps(dataSprint):
    aplicacion = dataSprint['Aplicación ']
    noSerepitenApps = []
    seRepiten = []
    for app in aplicacion:
        if app not in noSerepitenApps:
            noSerepitenApps.append(app)
        else:
            seRepiten.append(app)
            noSerepitenApps.remove(app)
    return seRepiten,noSerepitenApps

def addAppsNoRepeted(noSerepitenApps,dataSprint):
    consolidado = pd.DataFrame(columns=['Año','SPRINT','PITTs','Aplicación ','Tx E2E objetivo','Tx E2E Activas','% Cobertura E2E','Tx Reg objetivo','Tx Reg Activas','% Cobertura Reg','CP Manuales','CP Automáticos','CP Totales','Defectos Manuales','Defectos Automáticos','Defectos Totales','Impacto\nAlto','Impacto\nMedio','Impacto\nBajo','Area'])

    for apps in noSerepitenApps:
        dataFrameBase = dataSprint[dataSprint['Aplicación '] == apps]
        consolidado = consolidado.append(dataFrameBase, ignore_index=True,sort = False)
    return consolidado

def toListRowsCouple(seRepiten,dataSprint):
    appsList = []
    for app in seRepiten:
        dataFrameRows = dataSprint[dataSprint['Aplicación '] == app]
        appsList.append(dataFrameRows)
    return appsList

def consolidateRepeted(consolidado,appsList):
    dataGrupos = pd.DataFrame(columns = ['Año','SPRINT','PITTs','Aplicación ','Tx E2E objetivo',
                                       'Tx E2E Activas','% Cobertura E2E','Tx Reg objetivo','Tx Reg Activas',
                                       '% Cobertura Reg','CP Manuales','CP Automáticos','CP Totales',
                                       'Defectos Manuales','Defectos Automáticos','Defectos Totales',
                                       'Impacto\nAlto','Impacto\nMedio','Impacto\nBajo','Area'])
    for group in appsList:
        dataagrupada = group.loc[:,'Tx E2E objetivo':'Impacto\nBajo']
        dataSumada  = dataagrupada.sum()

        dataGrupos.at[0,'Año'] = max(group['Año'])
        dataGrupos.at[0,'SPRINT'] = max(group['SPRINT'])
        dataGrupos.at[0,'PITTs'] = max(group['PITTs'])
        dataGrupos.at[0,'Aplicación '] = max(group['Aplicación '])
        dataGrupos.at[0,'Tx E2E objetivo':'Impacto\nBajo'] = dataSumada
        dataGrupos.at[0,'Area'] = 'juntos'
        consolidado = consolidado.append(dataGrupos,ignore_index = True, sort = False)
    return consolidado

def comparate(seRepiten,noSeRepiten):
    for rapp in seRepiten:
        for app in noSeRepiten:
            if rapp == app:
                noSeRepiten.remove(app)
    return seRepiten,noSeRepiten


def consolidateData(datasetJoined):
    Sprint = getNextSprintNumberUpdate(datasetJoined)
    transformaciondata = addPittsTransformacion(datasetJoined,Sprint)
    dataFrameFiltredBySoporte = datasetJoined[datasetJoined['Area'] == 'Soporte']
    dataSprint = transformaciondata.append(dataFrameFiltredBySoporte,ignore_index = True, sort = False)
    dataSprint['Aplicación '] =  dataSprint['Aplicación '].str.upper()

    dataToAppended = datasetJoined[datasetJoined['SPRINT'] < Sprint]
    dataToAppended = dataToAppended[dataToAppended['Area'] == 'Soporte']
    dataSprint = dataSprint[dataSprint['SPRINT'] == Sprint]
    seRepiten,noSeRepiten = separateApps(dataSprint)
    repetidas,norepetidas = comparate(seRepiten,noSeRepiten)
    consolidado = addAppsNoRepeted(norepetidas,dataSprint)
    appsList = toListRowsCouple(repetidas,dataSprint)
    consolidadoFinal = consolidateRepeted(consolidado,appsList)
    dataToAppended = dataToAppended.append(consolidadoFinal,ignore_index = True, sort = False)
    dataToAppended = dataToAppended.sort_values(by = ['SPRINT'],ascending = False)
    return dataToAppended




def JoinDataSetFinals(transformacionDataset,soporteDataset,sprintNumber):
    datasetJoined =  transformacionDataset.append(soporteDataset)
    pathToExport='consolidado.xlsx'
    pathFinal=os.path.join(resourcesFiles,pathToExport)
    dataToAppended = consolidateData(datasetJoined)
    del dataToAppended['Area']
    dataToAppended.to_excel(pathFinal,index=False)
    print('exportado '+pathToExport)
