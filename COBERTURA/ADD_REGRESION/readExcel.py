import pandas as pd

def  buildDtf(files):
        data = pd.read_excel(files)
        return data
def  buildDtfS(files):
        data = pd.read_excel(files)
        data = data.rename(columns={'Aplicación': 'Aplicación '})
        data = data.rename(columns={'Impacto Alto': 'Impacto\nAlto'})
        data = data.rename(columns={'Impacto Medio': 'Impacto\nMedio'})
        data = data.rename(columns={'Impacto Bajo': 'Impacto\nBajo'})
        return data
