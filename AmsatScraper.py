import re
import requests
import numpy as np
import pandas as pd


def Fixer(row):
    #_case = get_case(row)
    if ('(bandwidth' in row):
        avg = row.split('(')[0]
        bw = row.replace(' ', '')[-6:-4]
        return avg, bw
    elif ('~' in row):
        return row.replace('~', ''), 'None'
    elif ('//' in row):
        entries = [Fixer(x) for x in row.split('//')]
        #print("ENTRIES: ", entries)
        indFreqs = entries[0][0], entries[1][0]
        indBands = entries[0][1], entries[1][1]
        returnedRow = indFreqs, indBands
        #print(returnedRow)
        return indFreqs, indBands
    elif ('/' in row):
        entries = [Fixer(x) for x in row.split('/')]
        indFreqs = entries[0][0], entries[1][0]
        indBands = entries[0][1], entries[1][1]
        returnedRow = indFreqs, indBands
        #print(returnedRow)
        return indFreqs, indBands
    elif ('-' in row):
        indFreqs = [float(x.strip()) for x in row.split('-')]
        avg = str(np.average(indFreqs))
        bw = str(abs(round((indFreqs[1]-indFreqs[0])/2, 6)) * 1000) + ' kHz'
        return avg, bw
    else:
        return row, 'None'

def Scraper():
    """
    Downloads an excel spreadsheet of amateur radio satellites
    monitored by AMSAT-UK.
    """

    amsat_url = "http://www.ne.jp/asahi/hamradio/je9pel/satslist.xls"

    #read spreadsheet and drop header
    amsat_xl = pd.read_excel(amsat_url, skiprows=10)

    #convert to dataframe, drop irrelevant columns.
    amsat_df = pd.DataFrame(amsat_xl)
    amsat = amsat_df

    #drop footer
    #amsat = amsat.iloc[:-48]

    #convert to dictionary
    amsat_dict = amsat.to_dict('list')

    actDict = {'*':'Active', 'd':'Deep Space', 'f':'Failure', 'i':'Inactive', 'n':'Non-amateur',
              'r':'Re-entered', 't':'To be launched', 'u':'Unknown', 'w':'Weather sat', 'nan':'None', 'c':'Canceled'}

    myDict = {'ID':[str(x) for x in amsat_dict.pop('Number')], 'Name':[str(x) for x in amsat_dict.pop('Satellite')],
             'Frequency':[str(x) for x in amsat_dict.pop('Downlink')], 'Bandwidth/Baud':[], 'Status':[actDict[str(x)] for x in amsat_dict.pop('Unnamed: 7')],
             'Description':[str(x) for x in amsat_dict.pop('Mode')], 'Source':[]}

    #Remove null entries

    beacons = [str(x) for x in amsat_dict.pop('Beacon')]
    ogLen = len(myDict['Frequency'])
    myDict['Frequency'] += beacons

    for key in myDict:
        if (key != 'Frequency'):
            myDict[key] += myDict[key]


    nulls = []
    index = 0
    for each in myDict['Name']:
        myDict['Source'] = myDict['Source'] + ['AmSAT']
        myDict['Bandwidth/Baud'] = myDict['Bandwidth/Baud'] + ['BW']
        if ((each == 'nan') or (myDict['Frequency'][index] == 'nan')):
            nulls += [index]
        if (myDict['Description'][index].strip() in actDict.keys()):
            myDict['Status'][index] = actDict[myDict['Description'][index].strip()]
            myDict['Description'][index] = 'None'
        if (index >= ogLen):
            myDict['Description'][index] = 'Beacon, ' + myDict['Description'][index]
        if (bool(re.search(r'\d', myDict['Frequency'][index])) == False):
            nulls += [index]

        index += 1

    nulls = (sorted(list(set(nulls)), reverse=True))

    for popInd in nulls:
        myDict['ID'].pop(popInd)
        myDict['Name'].pop(popInd)
        myDict['Frequency'].pop(popInd)
        myDict['Status'].pop(popInd)
        myDict['Description'].pop(popInd)
        myDict['Bandwidth/Baud'].pop(popInd)
        myDict['Source'].pop(popInd)

    freqLen = len(myDict['Frequency'])

    for ind in range(freqLen):
        indFreq = myDict['Frequency'][ind]
        if ((indFreq == ('U S-band 5.8GHz')) or (indFreq == ('S Ku-band'))):
            myDict['Bandwidth/Baud'][ind] = 'None'

        else:
            entries = Fixer(indFreq)
            if (len(entries[0]) == 2):
                myDict['Frequency'][ind] = entries[0][0]
                myDict['Bandwidth/Baud'][ind] = entries[1][0]
                myDict['Frequency'] = myDict['Frequency'] + [entries[0][1]]
                myDict['Bandwidth/Baud'] = myDict['Bandwidth/Baud'] + [entries[1][1]]
                for key in myDict:
                    if ((key != 'Frequency') and (key != 'Bandwidth/Baud')):
                        myDict[key] = myDict[key] + [myDict[key][ind]]
            else:
                myDict['Frequency'][ind] = entries[0]

                myDict['Bandwidth/Baud'][ind] = entries[1]

    return myDict

if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
