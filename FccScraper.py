import pandas as pd
import requests

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
             'Frequency':[str(x) for x in fcc_dict.pop('Frequency Range')], 'Description':[str(x) for x in fcc_dict.pop('Notes')]}
    myDict['Status'] = ['None' for x in myDict['Name']]
    myDict['ID'] = ['None' for x in myDict['Name']]

    #Remove null entries
    nulls = []

    for index in range(len(myDict['Frequency'])):
        nf = []

        if ((myDict['Name'][index] == 'nan') or (myDict['Frequency'][index] == 'nan')):
            nulls += [index]

        elif ('\n' in myDict['Frequency'][index]):
            nulls += [index]
            spl = myDict['Frequency'][index].split('\n')
            for each in spl:
                indLine = each.strip().split(' ')
                indFreq = indLine[0].split('-')
                print(indLine[1])
                if (indLine[1] == 'GHz'):
                    indFreq = [str(1000*float(x)) for x in indFreq]
                if ((indLine[1] != 'GHz') and (indLine[1] != 'MHz')):
                    pass
                if (len(indFreq) == 2):
                    nf += [indFreq[0] + '-' + indFreq[1]]
                else:
                    nf += [indFreq[0]]
            for newF in nf:
                myDict['ID'] += [myDict['ID'][index]]
                myDict['Name'] += [myDict['Name'][index]]
                myDict['Frequency'] += [newF]
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
