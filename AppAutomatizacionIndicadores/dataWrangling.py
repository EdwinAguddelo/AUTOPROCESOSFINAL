
from cleaners import *

def defectosDataWrangling(defectosDataset,Direccion,sprintNumber):

    defectosDataset=getDummiesFromDefectos(defectosDataset)
    defectosDataset=cleanDefectosDataFrame(defectosDataset)

    try:
        defectosDataset=defectosDataset.groupby(['Detected By']).get_group(Direccion)
        defectosDataset=defectosDataset.groupby(['Detected in Cycle']).get_group('Sprint'+str(sprintNumber))
        defectosDataset=defectosDataset.groupby(['Application','Detected in Cycle','Detected By']).sum()
    except:
        defectosDataset=defectosDataset.groupby(['Application','Detected in Cycle','Detected By']).sum()
        defectosDataset=defectosDataset.drop(defectosDataset.index, inplace=False)

    return defectosDataset

def casosPruebaDataWrangling(casosPruebasDataset,Direccion,sprintNumber):

    casosPruebasDataset=cleanCasosPruebaDataFrame(casosPruebasDataset,Direccion)    

    try:
        casosPruebasDataset=casosPruebasDataset.groupby(['Detected By']).get_group(Direccion)
        casosPruebasDataset=casosPruebasDataset.groupby(['SPRINT']).get_group('Sprint'+str(sprintNumber))
        casosPruebasDataset=casosPruebasDataset.groupby(['REL_NAME']).sum()
    except:
        casosPruebasDataset=casosPruebasDataset.groupby(['REL_NAME']).sum()
        casosPruebasDataset=casosPruebasDataset.drop(casosPruebasDataset.index, inplace=False)


    return casosPruebasDataset
