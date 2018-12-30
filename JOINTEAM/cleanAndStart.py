import pandas as pd
from JOINTEAM.StartJoin import *



def cleanTeamCol(dtfToclean):
    listateam = []
    for dt in dtfToclean:
        listateam.append(dt['EQUIPO'].tolist())
    for teamCol in listateam:
        for i,team in enumerate(teamCol):
            teamCol[i]=teamCol[i].split(' ')[0]
    return listateam

def StartProccessJoin(stj):
    dtCPMerged=stj.mergeCasosPrueba()
    dtDefectosMerged=stj.mergeDefectos()

    listateamCP=cleanTeamCol(dtCPMerged)
    listateamDef=cleanTeamCol(dtDefectosMerged)

    dtfCasosPrueba = JoinColCleaned(dtCPMerged,listateamCP)
    dtfDefectos = JoinColCleaned(dtDefectosMerged,listateamDef)

    filesDefectos=stj.getfileDefectos()
    filesCasosPrueba = stj.getfilesCasosPrueba()

    dtfDefectos = Deletecol(dtfDefectos)

    dtfCasosPrueba = changeNameColTeamCP(dtfCasosPrueba)
    dtfDefectos = changeNameColTeamDef(dtfDefectos)



    exportarAexcel(dtfCasosPrueba,filesCasosPrueba,'Query1')
    exportarAexcel(dtfDefectos,filesDefectos,'Sheet1')

def JoinColCleaned(dtMerged,listateam):
    for i,dt in enumerate(dtMerged):
        try:
            dt['EQUIPO']=pd.DataFrame(listateam[i])
        except Exception:
            pass
    return dtMerged



def changeNameColTeamCP(dtframesArray):
    for i,dt in enumerate(dtframesArray):
        try:
            dtframesArray[i] = dtframesArray[i].rename(columns = {'EQUIPO':'Detected By'})
        except Exception:
            dtframesArray[i]=pd.DataFrame(columns=['REL_NAME','SPRINT','REL_USER_TEMPLATE_01','RUN_MANUAL','RUN_AUTO','NOMBRETESSET','CY_CYCLE_ID','APLICATIVO','TIPOPRUEBA','Detected By'])
    return dtframesArray

def changeNameColTeamDef(dtframesArray):
    for i,dt in enumerate(dtframesArray):
        try:
            dtframesArray[i] = dtframesArray[i].rename(columns = {'EQUIPO':'Detected By'})
        except Exception:
            dtframesArray[i]=pd.DataFrame(columns=['Defect ID','Application','Defect Type','Detected in Cycle','Business Impact','Automatic Defect','Detected By'])
    return dtframesArray


def Deletecol(dtframesArray):
        for i,dtf in enumerate(dtframesArray):
            dtframesArray[i]=dtframesArray[i].drop(columns=['Detected By'])
        return dtframesArray

def exportarAexcel(dtfArray,filepath,shtName):
    for i,dtf in enumerate(dtfArray):
        dtf.to_excel(filepath[i],index=False,sheet_name=shtName)
        print('Exportado {}'.format(filepath[i]))
