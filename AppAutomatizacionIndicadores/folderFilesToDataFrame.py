import pandas as pd

def folderPathToDataFrames(FolderPath):
    DataFrames=[]
    for file in FolderPath:
        DataFrame=pd.read_excel(file)
        DataFrames.append(DataFrame)
    return DataFrames
