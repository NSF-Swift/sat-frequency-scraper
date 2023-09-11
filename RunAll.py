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
from CelesTrakScraper import Scraper as cts
from SpaceTrackScraper import Scraper as sts


def ScrapeAll():
    myDicts = [sts(), sns(), rgs(), fccs(), ams(), ucs(), cts()]





    IDs, names, freqs, bandW, stats, descs, sources, orbits = [], [], [], [], [], [], [], []
    for each in myDicts:
        IDs += each['ID']
        names += each['Name']
        freqs += each['Frequency']
        bandW += each['Bandwidth/Baud']
        stats += each['Status']
        descs += each['Description']
        sources += each['Source']
        orbits += each['Orbit']



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
    orbits = list(np.array(orbits)[nameInds])




    clones = []
    index = 0
    for each in names:
        eachInd = index + 1
        for rest in names[eachInd:]:
            if (rest.lower() == each.lower()):
                if ((freqs[index] == freqs[eachInd]) and (stats[index] == stats[eachInd]) and (descs[index] == descs[eachInd])):
                    clones += [eachInd]
                elif (freqs[index] == 'None'):
                    clones += [index]
                    IDs[eachInd] = IDs[index]
                    orbits[eachInd] = orbits[index]
                    sources[eachInd] = list(set(sources[eachInd] + ', ' + sources[index]))
                elif (freqs[eachInd] == 'None'):
                    clones += [eachInd]
                    IDs[index] = IDs[eachInd]
                    orbits[index] = orbits[eachInd]
                    sources[index] = list(set(sources[index] + ', ' + sources[eachInd]))

            eachInd += 1
        index += 1

    clones = sorted(list(set(clones)), reverse=True)


    compDict = {'ID':IDs, 'Name':names, 'Frequency [MHz]':freqs, 'Bandwidth [kHz]/Baud':bandW,
                'Status':stats, 'Description':descs, 'Source':sources, 'Orbit':orbits}

    for popInd in clones:
        for Key in compDict:
            compDict[Key].pop(popInd)

    for ind in range(len(compDict['Name'])):
        for Key in compDict:
            if (str(compDict[Key][ind]) == str(float('nan'))):
                compDict[Key][ind] = 'None'
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
