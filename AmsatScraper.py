import re
import requests
import numpy as np
import pandas as pd

def get_case(row):
    if '(bandwidth' in row:
        _case = 'parenthesis'
    elif '~' in row:
        _case = 'tilde'
    elif '//' in row:
        _case = 'dub_mult'
    elif '/' in row:
        _case = 'mult'
    elif '-' in row:
        _case = 'band'
    else:
        _case = 'single'
    return _case

def Fixer(row):
    _case = get_case(row)
    if _case == 'band':
        indFreqs = [float(x.strip()) for x in row.split('-')]
        avg = str(np.average(indFreqs))
        bw = str((indFreqs[1]-indFreqs[0])/2)
        return avg, bw
    elif _case == 'parenthesis':
        avg = row.split('(')[0]
        bw = row.replace(' ', '')[-6:-4] 
        return avg, bw
    elif _case == 'tilde':
        return row.replace('~', ''), 'None'
    elif _case == 'dub_mult':
        entries = [Fixer(x) for x in row.split('//')]
        indFreqs = entries[0][0], entries[0][1]
        indBands = entries[1][0], entries[1][1]
        return indFreqs, indBands
    elif _case == 'mult':
        entries = [Fixer(x) for x in row.split('/')]
        indFreqs = entries[0][0], entries[0][1]
        indBands = entries[1][0], entries[1][1]
        return indFreqs, indBands
    elif _case == 'single':
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

    newFreqs = []
    newBands = []
    for each in myDict['Frequency']:
        if each == ('U S-band 5.8GHz'):
            newFreqs.append(each)
            newBands.append('None')
        elif each == ('S Ku-band'):
            newFreqs.append(each)
            newBands.append('None')
        else:
            newFreqs.append(Fixer(each)[0])
            newBands.append(Fixer(each)[1])

    myDict['Frequency'] = newFreqs
    myDict['Bandwidth/Baud'] = newBands

    return myDict

if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
