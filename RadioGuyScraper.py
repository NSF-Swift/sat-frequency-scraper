import mechanicalsoup
import requests
import pandas as pd
import numpy as np

def Scraper():
    """
    Returns dictionary consisting of ID, Name, Frequency, Status, and Description
    """
    rg_url = "https://usradioguy.com/NOAA/Satellite_Frequencies_2023-03-01.xlsx"

    #read spreadsheet and convert into dataframe
    rg_xl = pd.read_excel(rg_url)
    rg_df = pd.DataFrame(rg_xl)

    #convert to dictionary
    rg_dict = rg_df.to_dict('list')


    myDict = {'Name':[str(x) for x in rg_dict.pop('Satellite')],
             'Frequency':[str(x[:x.index("M")].strip()) for x in rg_dict.pop('Frequency (MHz)')],
              'Bandwidth/Baud':[str(x) for x in rg_dict.pop('Bandwidth (kHz)')],
              'Description':[str(x) for x in rg_dict.pop('Comment')],
              'Status':[str(x) for x in rg_dict.pop('Dead/Active')]}
    myDict['ID'] = ['None' for x in myDict['Name']]
    myDict['Orbit'] = ['None' for x in myDict['Name']]
    myDict['Source'] = ['USRadioGuy' for x in myDict['Name']]

    newStat = []
    for each in myDict['Status']:
        if (each == 'D'):
            stat = 'inactive'
        else:
            stat = 'active'
        newStat += [stat]
    myDict['Status'] = newStat

    for index in range(len(myDict['Frequency'])):
        each = myDict['Frequency'][index]
        if ('-' in each):
            indFreqs = [float(x.strip()) for x in each.split('-')]
            newF = str(np.average(indFreqs))
            myDict['Frequency'][index] = newF

    return myDict





if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
