from datetime import datetime
from utils import getNextSprintNumber

class TransformacionRow(object):

    def __init__(self,app,sprintNumber,feed,FileName):

        self.Anho=datetime.now().year
        self.SPRINT=sprintNumber
        self.PITTs=FileName.split('/')[-1].split('.')[0]
        self.Aplicacion=app
        self.TxE2Eobjetivo=''
        self.TxE2EActivas=''
        self.CoberturaE2E=''
        self.TxRegobjetivo=''
        self.TxRegActivas=''
        self.CoberturaReg=''

        self.CPManuales=feed['CPManuales']
        self.CPAutomáticos=feed['CPAutomáticos']
        self.CPTotales=feed['CPTotales']

        self.DefectosManuales=feed['DefectosManuales']
        self.DefectosAutomáticos=feed['DefectosAutomáticos']
        self.DefectosTotales=feed['DefectosTotales']
        self.ImpactoAlto=feed['ImpactoAlto']
        self.ImpactoMedio=feed['ImpactoMedio']
        self.ImpactoBajo=feed['ImpactoBajo']

        #self.SPRINT2='({})'.format(self.SPRINT)

    def getRow(self):
        return [self.Anho,self.SPRINT,self.PITTs,self.Aplicacion,self.TxE2Eobjetivo,self.TxE2EActivas,self.CoberturaE2E,self.TxRegobjetivo,self.TxRegActivas,self.CoberturaReg,self.CPManuales,self.CPAutomáticos,self.CPTotales,self.DefectosManuales,self.DefectosAutomáticos,self.DefectosTotales,self.ImpactoAlto,self.ImpactoMedio,self.ImpactoBajo]


def rowFeeder(releaseName,defectosSumaDataFrame,casosPruebaSumaDataSet):

    CPManuales=0
    CPAutomáticos=0
    CPTotales=0
    DefectosManuales=0
    DefectosAutomáticos=0
    DefectosTotales=0
    ImpactoAlto=0
    ImpactoMedio=0
    ImpactoBajo=0

    for appsEnListaCasosPrueba in casosPruebaSumaDataSet.index.get_level_values(0).tolist():
        if appsEnListaCasosPrueba in releaseName:
            duda=casosPruebaSumaDataSet.groupby(['REL_NAME']).get_group(appsEnListaCasosPrueba)

            CPManuales=duda['RUN_MANUAL'].values.tolist()[0]
            CPAutomáticos=duda['RUN_AUTO'].values.tolist()[0]
            CPTotales=CPManuales+CPAutomáticos

    for appsEnListaDefectos in defectosSumaDataFrame.index.get_level_values(0).tolist():

        if appsEnListaDefectos in releaseName:
            duda=defectosSumaDataFrame.groupby(['Application']).get_group(appsEnListaDefectos)
            duda.index=duda.index.droplevel(1)
            duda.index=duda.index.droplevel(1)
            duda=duda.loc[duda.index == appsEnListaDefectos]

            DefectosManuales=duda['Automatic Defect_N'].values.tolist()[0]
            try:
                DefectosAutomáticos=duda['Automatic Defect_Y'].values.tolist()[0]
            except KeyError:
                DefectosAutomáticos=0
            DefectosTotales=DefectosManuales+DefectosAutomáticos
            ImpactoAlto=duda['Business Impact_A-High'].values.tolist()[0]
            ImpactoMedio=duda['Business Impact_B-Medium'].values.tolist()[0]
            ImpactoBajo=duda['Business Impact_C-Low'].values.tolist()[0]

    feed={
        'CPManuales':CPManuales,
        'CPAutomáticos':CPAutomáticos,
        'CPTotales':CPTotales,
        'DefectosManuales':DefectosManuales,
        'DefectosAutomáticos':DefectosAutomáticos,
        'DefectosTotales':DefectosTotales,
        'ImpactoAlto':ImpactoAlto,
        'ImpactoMedio':ImpactoMedio,
        'ImpactoBajo': ImpactoBajo
    }

    return feed
