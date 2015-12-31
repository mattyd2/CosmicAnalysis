import numpy as np
import pandas as pd

# how to find unique windows with maximum mutational meancountsquared.

def mutationNT(listOfDFsByGene):
    listOfMeansPerSliceDF = []
    for DFforGene in listOfDFsByGene:
        ntlist = np.array(DFforGene['NT'])
        listofStartIndicestosliceon, listofEndIndicestosliceon = find_nearest(ntlist)
        listofslices = slicefunction(DFforGene, listofStartIndicestosliceon, listofEndIndicestosliceon)
        listOfMeansPerSliceDF.append(getmeanfunction(listofslices)) # this should have all columns plus Start NT, End NT, Mean Mutations
    return listOfMeansPerSliceDF

def getmeanfunction(listofslices):
    columns = ['Gene', 'StartNT', 'EndNT', 'NTWindowSize', 'SumMutationCount', 'MeanCount'] # To Do - http://stackoverflow.com/questions/19112398/getting-list-of-lists-into-pandas-dataframe
    newDataFrame = pd.DataFrame(columns=columns) # simplify Dataframe creation
    countList, genelist, firstNTlist, lastNTlist, meanList = [],[],[],[],[]
    for x in listofslices:
        lastNTValue = x["NT"].iloc[-1]
        firstNTValue = x["NT"].iloc[0]
        firstGENEValue = x["Gene"].iloc[0]
        meadValue = x["Count"].mean(axis=0)
        countTotal = x["Count"].sum(axis=0)
        countList.append(countTotal)
        genelist.append(firstGENEValue)
        firstNTlist.append(firstNTValue)
        lastNTlist.append(lastNTValue)
        meanList.append(meadValue)
    newDataFrame['Gene'] = genelist
    newDataFrame['StartNT'] = firstNTlist
    newDataFrame['EndNT'] = lastNTlist
    newDataFrame['NTWindowSize'] = newDataFrame['EndNT'] - newDataFrame['StartNT']
    newDataFrame['SumMutationCount'] = countList
    newDataFrame['MeanCount'] = meanList
    newDataFrame['MeanCountSquared'] = newDataFrame['MeanCount']*newDataFrame['MeanCount']
    finalDataFrame = newDataFrame.sort_values('MeanCountSquared', ascending=False, inplace=False)
    finalDataFrame.reset_index(inplace=True)
    return finalDataFrame

def slicefunction(DFforGenetoSlice, listofStartIndicestosliceon, listofEndIndicestosliceon):
    listofslicedDFs = []
    for x, y in zip(listofStartIndicestosliceon, listofEndIndicestosliceon): # might need to change this to iteratertools if the lists become very large
        sliceddataframeTemp = DFforGenetoSlice.iloc[x:y]
        listofslicedDFs.append(sliceddataframeTemp)
    return listofslicedDFs

def find_nearest(array):
    listofStartIndices = []
    listofEndIndices = []
    arraySize = array.size
    for idx, x in enumerate(array):
        incrementor = x + 150
        insertIndex = np.searchsorted(array, incrementor)
        if insertIndex < arraySize:
            insertIndexValue = array[insertIndex]
            if incrementor <= insertIndexValue:
                insertIndex = insertIndex - 1
                insertIndexValue = array[insertIndex]
            windowSize = insertIndexValue - x
            if windowSize > 100:
                listofStartIndices.append(idx)
                listofEndIndices.append(insertIndex)
    return listofStartIndices, listofEndIndices
