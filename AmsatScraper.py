import pandas as pd
import requests

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
    amsat = amsat_df.drop(['Mode'], axis=1)

    #drop footer
    #amsat = amsat.iloc[:-48]

    #convert to dictionary
    amsat_dict = amsat.to_dict('list')

    actDict = {'*':'Active', 'd':'Deep Space', 'f':'Failure', 'i':'Inactive', 'n':'Non-amateur',
              'r':'Re-entered', 't':'To be launched', 'u':'Unknown', 'w':'Weather sat', 'nan':'None'}
    myDict = {'ID':[str(x) for x in amsat_dict.pop('Number')], 'Name':[str(x) for x in amsat_dict.pop('Satellite')],
             'Frequency':[str(x) for x in amsat_dict.pop('Downlink')], 'Status':[actDict[str(x)] for x in amsat_dict.pop('Unnamed: 7')]}
    myDict['Description'] = ['None' for x in myDict['ID']]

    #Remove null entries



    nulls = []
    index = 0
    for each in myDict['Name']:
        if ((each == 'nan') or (myDict['Frequency'][index] == 'nan')):
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
