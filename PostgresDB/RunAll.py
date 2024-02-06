import mechanicalsoup
import requests
import pandas as pd
import numpy as np
import os
import sys
import progressbar
from sqlalchemy import create_engine

parent_directory = os.path.abspath('..')
sys.path.append(parent_directory)

### Import Scrapers
from RadioGuyScraper import Scraper as rgs
#from SatNogsScraper import Scraper as sns
from FccScraper import Scraper as fccs
from AmsatScraper import Scraper as ams
from UCSScraper import Scraper as ucs
from CelesTrakScraper import Scraper as cts
from SpaceTrackScraper import Scraper as sts
from OscarScraper import Scraper as oscs


def ScrapeAll():
    #myDicts = [sts(), sns(), rgs(), fccs(), ams(), ucs(), cts(), oscs()]
    #Without Satnogs for now:
    myDicts = [sts(), rgs(), fccs(), ams(), ucs(), cts(), oscs()]




    print("Dictionaries collected")
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

    print("Mega Dictionary created")

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



    print("Finding cloned entries")
    clones = []
    index = 0

    widgets = ['Loading: ', progressbar.Bar('|')]

    bar = progressbar.ProgressBar(maxval=(len(names) - 1), widgets=widgets).start()
    for each in names:
        eachInd = index + 1
        bar.update(index)
        #print(index)
        for rest in names[eachInd:]:
            if (rest.lower() == each.lower()):
                if ((freqs[index] == freqs[eachInd]) and (stats[index] == stats[eachInd]) and (descs[index] == descs[eachInd])):
                    clones += [eachInd]
                elif (freqs[index] == 'None'):
                    clones += [index]
                    IDs[eachInd] = IDs[index]
                    orbits[eachInd] = orbits[index]
                    sources[eachInd] = sources[eachInd] + ', ' + sources[index]
                elif (freqs[eachInd] == 'None'):
                    clones += [eachInd]
                    IDs[index] = IDs[eachInd]
                    orbits[index] = orbits[eachInd]
                    sources[index] = sources[index] + ', ' + sources[eachInd]

            eachInd += 1
        index += 1

    clones = sorted(list(set(clones)), reverse=True)
    print("Clones found")

    compDict = {'ID':IDs, 'Name':names, 'Frequency [MHz]':freqs, 'Bandwidth [kHz]/Baud':bandW,
                'Status':stats, 'Description':descs, 'Source':sources, 'Orbit':orbits}

    for popInd in clones:
        for Key in compDict:
            compDict[Key].pop(popInd)
    print("Clones removed")

    for ind in range(len(compDict['Name'])):
        srcList = [x.strip() for x in compDict['Source'][ind].split(',')]
        compDict['Source'][ind] = ", ".join(str(x) for x in list(set(srcList)))
        for Key in compDict:
            if (str(compDict[Key][ind]) == str(float('nan'))):
                compDict[Key][ind] = 'None'
    print("Joining entries")

        #compDict['ID'].pop(popInd)
        #compDict['Name'].pop(popInd)
        #compDict['Frequency [MHz]'].pop(popInd)
        #compDict['Bandwidth [kHz]/Baud'].pop(popInd)
        #compDict['Status'].pop(popInd)
        #compDict['Description'].pop(popInd)
        #compDict['Source'].pop(popInd)



    return compDict

if __name__ == "__main__":
    print("Creating engine")
    engine = create_engine('postgresql://bstover:postgres@localhost/satfreqdb')
    myDict = ScrapeAll()
    sqlDict = {'id':myDict['ID'], 'name':myDict['Name'], 'frequency':myDict['Frequency [MHz]'], 'bandwidth':myDict['Bandwidth [kHz]/Baud'],
                'status':myDict['Status'], 'description':myDict['Description'], 'source':myDict['Source'], 'orbit':myDict['Orbit']}
    myFrame = pd.DataFrame.from_dict(sqlDict)

    #compDict = ScrapeAll()
    myFrame.to_sql('satfreqdb', engine)
    #myFrame.to_csv('SatList.csv', index=True)
