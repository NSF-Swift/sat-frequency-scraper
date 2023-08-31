import mechanicalsoup
import requests
import pandas as pd
import numpy as np

### Import Scrapers
from RadioGuyScraper import Scraper as rgs
from SatNogsScraper import Scraper as sns
from FccScraper import Scraper as fccs
from AmsatScraper import Scraper as ams
from UCSScraper import Scraper as ucs


def ScrapeAll():
    myDicts = [sns(), rgs(), fccs(), ams()]





    IDs, names, freqs, bandW, stats, descs, sources = [], [], [], [], [], [], []
    for each in myDicts:
        IDs += each['ID']
        names += each['Name']
        freqs += each['Frequency']
        bandW += each['Bandwidth/Baud']
        stats += each['Status']
        descs += each['Description']
        sources += each['Source']



    """
    Here we wish to add orbital class info if available
    """
    
    """
    orbits = ['None' for x in names]
    ucsDict = ucs()

    for nameInd in range(len(names)):
        if ((names[nameInd] in ucsDict['Friendly Name']) or (names[nameInd] in ucsDict['Official Name'])
            or (IDs[nameInd] in ucsDict['ID'])):
            if (IDs[nameInd] not in ucsDict['ID']):
                print(IDs[nameInd])
                print(names[nameInd])
            print("1")
        else:
            print("3")
    """


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
    sources = list(np.array(sources)[nameInds])

    compDict = {'ID':IDs, 'Name':names, 'Frequency [MHz]':freqs, 'Bandwidth [kHz]/Baud':bandW,
                'Status':stats, 'Description':descs, 'Source':sources}


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
        for Key in compDict:
            compDict[Key].pop(popInd)
        #compDict['ID'].pop(popInd)
        #compDict['Name'].pop(popInd)
        #compDict['Frequency [MHz]'].pop(popInd)
        #compDict['Bandwidth [kHz]/Baud'].pop(popInd)
        #compDict['Status'].pop(popInd)
        #compDict['Description'].pop(popInd)
        #compDict['Source'].pop(popInd)



    return compDict

if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(ScrapeAll())
    myFrame.to_csv('SatList.csv', index=True)
