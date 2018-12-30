import pandas as pd

def getDummiesFromDefectos(dataSetToDummieDataFrame):
    return pd.get_dummies(columns=['Business Impact','Automatic Defect'],data=dataSetToDummieDataFrame)


def cleanDefectosDataFrame(Dataset):
    Dataset=Dataset.drop('Defect ID', axis=1)

    try:
        a=Dataset.groupby(['Automatic Defect_N']).get_group(1)

        a['Business Impact_A-High']=0
        a['Business Impact_B-Medium']=0
        a['Business Impact_C-Low']=0
    ## Cambios
    except:
        a=Dataset
        a['Business Impact_A-High']=0
        a['Business Impact_B-Medium']=0
        a['Business Impact_C-Low']=0

        a=a.drop(a.index, inplace=False)
    # Cambios
    try:
        b=Dataset.groupby(['Automatic Defect_N']).get_group(0)
        defectosCanalesLimpios=a.append(b)
    except:
        defectosCanalesLimpios=a

    return defectosCanalesLimpios

def cleanCasosPruebaDataFrame(casosPruebaDataFrame,consolidado):

    releasesDataFrame=casosPruebaDataFrame['REL_NAME'].tolist()
    nombresDeAplicativo=casosPruebaDataFrame['APLICATIVO'].tolist()
    casosPruebaCanalesLimpioDataFrame = casosPruebaDataFrame

    casoPruebaCanalesDataFrame=[]
    for idx, val in enumerate(releasesDataFrame):
        if consolidado=='Transformacion': casoPruebaCanalesDataFrame.append('{}'.format(nombresDeAplicativo[idx]))
        elif consolidado=='Soporte': casoPruebaCanalesDataFrame.append('{}'.format(nombresDeAplicativo[idx]))

    if not len(casoPruebaCanalesDataFrame): casoPruebaCanalesDataFrame.append('')

    casosPruebaCanalesLimpioDataFrame=casosPruebaCanalesLimpioDataFrame.reset_index().drop('index', axis=1)
    try:
        casosPruebaCanalesLimpioDataFrame['REL_NAME']=pd.DataFrame(casoPruebaCanalesDataFrame)
    except Exception:
        pass
    casosPruebaCanalesLimpioDataFrame=casosPruebaCanalesLimpioDataFrame.drop('CY_CYCLE_ID', axis=1)

    return casosPruebaCanalesLimpioDataFrame
