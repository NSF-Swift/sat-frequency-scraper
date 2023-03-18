import pandas as pd
import requests
import re
import numpy as np

def entry_parser(Freq):
    spl = [x.replace(" ", "") for x in Freq.split('\n')]
    #print(spl)
    nf = []
    for each in spl:
        indFreqs = re.findall(r"[-+]?(?:\d*\.*\d+)", each)
        if ('GHz' in each):
            indFreqs = [str(1000*float(x)) for x in indFreqs]
        if (('GHz' not in each) and ('MHz' not in each)):
            continue
        if (len(indFreqs) == 2):
            if ('-' not in indFreqs[1]):
                continue
            nf += [indFreqs[0] + indFreqs[1]]
        elif (len(indFreqs) == 4):
            nf += [indFreqs[0] + indFreqs[1], indFreqs[2] + indFreqs[3]]
        else:
            nf += [indFreqs[0]]
    return nf






def Scraper():
    """
    Downloads an excel spreadsheet of space stations authorized by the FCC
    and converts it into a pandas dataframe.
    """

    fcc_url = "https://transition.fcc.gov/ib/sd/se/ssal.xlsx"

    #read spreadsheet and convert into dataframe
    fcc_xl = pd.read_excel(fcc_url)
    fcc_df = pd.DataFrame(fcc_xl)

    #drop irrelevant columns
    fcc = fcc_df.drop(['Orbital Location',
        'Licensee or Grantee',
        'Administration',
        'Service',
        'Date In-orbit and Operating',
        'Polarization & Coverage Information',
        'Orbital Debris Information',
        '47 CFR 25.140(d) Notice',
        '24/7 Contact',
        'Grant'
        ],
        axis=1
    )


    #convert to dictionary
    fcc_dict = fcc.to_dict('list')


    myDict = {'Name':[str(x) for x in fcc_dict.pop('Satellite Name')],
             'Frequency':[str(x) for x in fcc_dict.pop('Frequency Range')], 'Bandwidth/Baud':[], 'Description':[str(x) for x in fcc_dict.pop('Notes')]}
    myDict['Status'] = ['None' for x in myDict['Name']]
    myDict['ID'] = ['None' for x in myDict['Name']]

    #Remove null entries
    nulls = []

    for index in range(len(myDict['Frequency'])):
        nf = []

        if ((myDict['Name'][index] == 'nan') or (myDict['Frequency'][index] == 'nan')):
            nulls += [index]

        #elif ('\n' in myDict['Frequency'][index]):
        else:
            nulls += [index]
            #nf = [x.replace(" ", "") for x in spl] #I will change this eventually
            nf = entry_parser(myDict['Frequency'][index])
            for newF in nf:
                twoF = [float(x) for x in newF.split('-')]
                if (len(twoF) == 2):
                    bw = np.around((max(twoF) - min(twoF)), 4)
                    centerF = np.around(min(twoF) + (bw/2.), 4)
                    bw = bw*1000
                else:
                    bw = 'None'
                    centerF = twoF[0]
                myDict['ID'] += [myDict['ID'][index]]
                myDict['Name'] += [myDict['Name'][index]]
                myDict['Frequency'] += [str(centerF)]
                myDict['Bandwidth/Baud'] += [str(bw) + ' kHz']
                myDict['Status'] += [myDict['Status'][index]]
                myDict['Description'] += [myDict['Description'][index]]


    nulls = sorted(list(set(nulls)), reverse=True)

    for popInd in nulls:
        myDict['ID'].pop(popInd)
        myDict['Name'].pop(popInd)
        myDict['Frequency'].pop(popInd)
        myDict['Status'].pop(popInd)
        myDict['Description'].pop(popInd)


    return myDict

if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
