from datetime import datetime
import unicodedata
import pandas as pd
from ADD_REGRESION.DesignStart import *
from ADD_REGRESION.utils import getNextSprintNumber



def addYear(RegresiondataSet):
    RegresiondataSet['AÑO'] = datetime.now().year
    columna = RegresiondataSet['AÑO']
    del RegresiondataSet['AÑO']
    del RegresiondataSet['Código de la Aplicación']
    RegresiondataSet['Aplicación '] = RegresiondataSet['Aplicación '].str.upper()
    RegresiondataSet.insert(0,'Año',columna)
    RegresiondataSet = RegresiondataSet.fillna(0)

    return RegresiondataSet

def AppendDataFrames(soportedataSet,RegresiondataSet):
    ConsolidadoDT = soportedataSet.append(RegresiondataSet,sort=False)
    ConsolidadoDT = ConsolidadoDT.sort_values(by=['SPRINT'],ascending=False)
    ConsolidadoDT['Aplicación '] = ConsolidadoDT['Aplicación '].str.upper()

    return ConsolidadoDT

def cleanSpaces(SoporteConsolidadoDT):
    limpiar = []
    for app in SoporteConsolidadoDT['Aplicación ']:
        app = unicodedata.normalize("NFKD",app)
        limpiar.append(app)

    SoporteConsolidadoDT = SoporteConsolidadoDT.reset_index().drop('index', axis=1)
    SoporteConsolidadoDT['Aplicación '] = pd.DataFrame(limpiar)

    return SoporteConsolidadoDT

def findRepetedData(SoporteConsolidadoDT):
    apps = SoporteConsolidadoDT['Aplicación '].tolist()
    noAppsRepeted = []
    serepite =[]
    for app in apps:
        app = unicodedata.normalize("NFKD",app)
        if app not in noAppsRepeted:
            noAppsRepeted.append(app)
        else:
            serepite.append(app)
            noAppsRepeted.remove(app)
    for rapp in serepite:
        for app in noAppsRepeted:
            if rapp == app:
                noAppsRepeted.remove(app)

    return serepite,noAppsRepeted

def selectDataOfDataFrame(noSerepitenApps,SoporteFiltradoDT):
    consolidado = pd.DataFrame(columns=['Año','SPRINT','PITTs','Aplicación ','Tx E2E objetivo','Tx E2E Activas','% Cobertura E2E','Tx Reg objetivo','Tx Reg Activas','% Cobertura Reg','CP Manuales','CP Automáticos','CP Totales','Defectos Manuales','Defectos Automáticos','Defectos Totales','Impacto\nAlto','Impacto\nMedio','Impacto\nBajo'])
    for apps in noSerepitenApps:
        dataFrameBase = SoporteFiltradoDT[SoporteFiltradoDT['Aplicación '] == apps]
        consolidado = consolidado.append(dataFrameBase, ignore_index=True,sort = False)

    return consolidado

def appendFinalData(seRepiten,dataSprint,consolidado):
    appsList = []
    for app in seRepiten:
        dataFrameRows = dataSprint[dataSprint['Aplicación '] == app]
        appsList.append(dataFrameRows)


    dataGrupos = pd.DataFrame(columns = ['Año','SPRINT','PITTs','Aplicación ','Tx E2E objetivo',
                                       'Tx E2E Activas','% Cobertura E2E','Tx Reg objetivo','Tx Reg Activas',
                                       '% Cobertura Reg','CP Manuales','CP Automáticos','CP Totales',
                                       'Defectos Manuales','Defectos Automáticos','Defectos Totales',
                                       'Impacto\nAlto','Impacto\nMedio','Impacto\nBajo'])

    for group in appsList:
        dataagrupada = group.loc[:,'Tx E2E objetivo':'Impacto\nBajo']
        dataSumada  = dataagrupada.sum()

        dataGrupos.at[0,'Año'] = max(group['Año'])
        dataGrupos.at[0,'SPRINT'] = max(group['SPRINT'])
        dataGrupos.at[0,'PITTs'] = max(group['PITTs'])
        dataGrupos.at[0,'Aplicación '] = max(group['Aplicación '])
        dataGrupos.at[0,'Tx E2E objetivo':'Impacto\nBajo'] = dataSumada
        consolidado = consolidado.append(dataGrupos,ignore_index = True, sort = False)
    return consolidado

def exportarAexcel(datasetFinal,filepath):
        datasetFinal.to_excel(filepath,index=False)
        print('Exportado a {}'.format(filepath))



def startProcess(dgs):
    Regresionfile = dgs.getfileRegresion()
    soportefile = dgs.getfilesSoporteDT()

    soporteRute = dgs.getSoporteRute()
    sprintActual = getNextSprintNumber(soportefile)

    RegresionDataF = addYear(Regresionfile)

    SoporteDataF = AppendDataFrames(soportefile,RegresionDataF)
    dataSprint = SoporteDataF[SoporteDataF['SPRINT'] == sprintActual]
    SoporteDataF = cleanSpaces(SoporteDataF)
    SoporteDataF = SoporteDataF[SoporteDataF["SPRINT"] < sprintActual]


    AppsRepeted,noserepite = findRepetedData(dataSprint)
    consolidadoAppsNoRepetidas = selectDataOfDataFrame(noserepite,dataSprint)
    DataFrameFinal = appendFinalData(AppsRepeted,dataSprint,consolidadoAppsNoRepetidas)
    consolidado = SoporteDataF.append(DataFrameFinal,ignore_index = True, sort = False)
    consolidado = consolidado.sort_values(by=['SPRINT'],ascending=False)
    exportarAexcel(consolidado,soporteRute)
