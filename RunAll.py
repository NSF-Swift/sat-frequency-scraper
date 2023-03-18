import mechanicalsoup
import requests
import pandas as pd
import numpy as np

### Import Scrapers
from RadioGuyScraper import Scraper as rgs
from SatNogsScraper import Scraper as sns
from FccScraper import Scraper as fccs
from AmsatScraper import Scraper as ams

myDicts = [sns(), rgs(), fccs()]





IDs, names, freqs, bandW, stats, descs = [], [], [], [], [], []
for each in myDicts:
    IDs += each['ID']
    names += each['Name']
    freqs += each['Frequency']
    bandW += each['Bandwidth/Baud']
    stats += each['Status']
    descs += each['Description']

"""
Sort based off Names
"""

nameInds = np.argsort(np.array(names))
names = list(np.array(names)[nameInds])
IDs = list(np.array(IDs)[nameInds])
freqs = list(np.array(freqs)[nameInds])
bandW = list(np.array(bandW)[nameInds])
stats = list(np.array(stats)[nameInds])
descs = list(np.array(descs)[nameInds])

compDict = {'ID':IDs, 'Name':names, 'Frequency [MHz]':freqs, 'Bandwidth [kHz]/Baud':bandW, 'Status':stats, 'Description':descs}


clones = []
index = 0
for each in names:
    eachInd = index + 1
    for rest in names[eachInd:]:
        if (rest == each):
            if ((freqs[index] == freqs[eachInd]) and (stats[index] == stats[eachInd]) and (descs[index] == descs[eachInd])):
                clones += [eachInd]
        eachInd += 1
    index += 1

clones = sorted(list(set(clones)), reverse=True)


for popInd in clones:
    compDict['ID'].pop(popInd)
    compDict['Name'].pop(popInd)
    compDict['Frequency [MHz]'].pop(popInd)
    compDict['Bandwidth [kHz]/Baud'].pop(popInd)
    compDict['Status'].pop(popInd)
    compDict['Description'].pop(popInd)



myFrame = pd.DataFrame.from_dict(compDict)
#print(sorted(names))
myFrame.to_csv('SatList.csv', index=True)
