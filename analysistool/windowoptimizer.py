import pandas as pd
import numpy as np

def windowBuilder(calculatedDFsMutations):
    for singleDF in calculatedDFsMutations:
        tempDF = windowChecker(singleDF)

def windowChecker(dfOfMutations):
    firstRow = dfOfMutations[:1]
    numberOfRows = np.arange(1, dfOfMutations.shape[0])
    it = iter(numberOfRows)
    finalListOfStartandEndNT = []
    for x in it:
        nextX = next(it)
        startNTValue = np.array(dfOfMutations.StartNT[x:nextX])
        endNTValue = np.array(dfOfMutations.EndNT[x:nextX])
        interval = [int(startNTValue), int(endNTValue)]
        finalListOfStartandEndNT.append(interval)
    return overlapChecker(finalListOfStartandEndNT)

def overlapChecker(listOfStartandEndNT):
    firstValue = listOfStartandEndNT[0][0]
    lastValue = listOfStartandEndNT[0][1]
    for i,j in listOfStartandEndNT:
        print i,j
