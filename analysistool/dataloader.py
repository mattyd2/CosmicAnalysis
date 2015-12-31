import numpy as np
import pandas as pd
import re

def loaddata():
    loadeddata = pd.read_csv("/Users/matthewdunn/Dropbox/CosmicAnalysis/Raw_Data.csv")
    return getNTvalue(loadeddata)

def getNTvalue(dataSplitting):
    name = dataSplitting.MutationCDS
    newlist = list(name.values)
    myre = '((\d{4})(?=\D{1})|(\d{3})(?=\D{1})|(\d{2})(?=\D{1}))'
    finallist = []
    for x in newlist:
        y = re.search(myre,x)
        if y != None:
            finallist.append(y.group(1))
        else:
            finallist.append("")
    dataSplitting['NT'] = finallist
    dataSplitting.NT = dataSplitting.NT.replace('',np.nan)
    return prepData(dataSplitting)
    # TO DO - Yes that is why I had a consolidate formula which adds all the mutations at that one position.

def prepData(dataTypeChange):
    dataTypeChange.dropna(axis=0, how='any', inplace=True)
    dataTypeChange.loc[:,('Count','NT')] = dataTypeChange.loc[:,('Count','NT')].astype(int)
    return getDFPerGene(dataTypeChange)

def getDFPerGene(dataToSplitGene):
    geneList = pd.unique(dataToSplitGene.Gene.ravel())
    listofdfs = []
    for x in geneList:
        geneSpecificDF = dataToSplitGene.loc[dataToSplitGene['Gene'] == x]
        geneSpecificDF.sort_values('NT', axis=0, inplace=True)
        listofdfs.append(geneSpecificDF)
    return listofdfs

def csvwriter(DFtoWrite):
    incrementer = 0
    for x in DFtoWrite:
        geneValue = x['Gene'].iloc[:1]
        name = geneValue.values
        x.to_csv(str(name)+'.csv', encoding='utf-8')
