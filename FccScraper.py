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

    #drop footer
    fcc = fcc.iloc[:-23]

    #convert to dictionary
    fcc_dict = fcc.to_dict('list')
    myDict = fcc_dict

    myDict = {'ID':[str(x) for x in fcc_dict.pop('Call Sign')], 'Name':[str(x) for x in fcc_dict.pop('Satellite Name')],
             'Frequency':[str(x) for x in fcc_dict.pop('Frequency Range')], 'Description':[str(x) for x in fcc_dict.pop('Notes')]}
    myDict['Status'] = ['None' for x in myDict['ID']]

    #Remove null entries



    nulls = []
    index = 0
    for each in myDict['Name']:
        if (each == 'nan'):
            nulls += [index]
        index += 1

    nulls = sorted(nulls, reverse=True)

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
