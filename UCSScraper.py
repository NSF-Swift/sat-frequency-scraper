import pandas as pd
import requests
import re
import numpy as np

"""
This script returns a dictionary with different keys than the others. That is -
Friendly Name, Alternate Names, ID, and Orbit Class. The idea is to use this
script to fill in the Orbit Class column for listed satellites
"""

def Scraper():
    ucs_url = "https://www.ucsusa.org/media/11492"

    ucs_xl = pd.read_excel(ucs_url, storage_options={'User-Agent': 'Chrome/51.0.2704.103'})
    ucs_df = pd.DataFrame(ucs_xl)

    ucs_dict = ucs_df.to_dict('list')

    names = ucs_dict['Name of Satellite, Alternate Names']

    friendly_names = []
    alternate_names = []

    for indName in names:
        name_list = indName.split("(")
        friendly = name_list[0].strip()
        if (len(name_list) == 1):
            alternate = 'null'
        else:
            alternate = name_list[1].split(")")[0].strip()

        friendly_names += [friendly]
        alternate_names += [alternate]

    myDict = {'Name':[str(x) for x in ucs_dict.pop('Current Official Name of Satellite')], 'Friendly Name':friendly_names, 'Alternate Names':alternate_names,
            'ID':[str(x) for x in ucs_dict.pop('NORAD Number')], 'Orbit':[str(x) for x in ucs_dict.pop('Class of Orbit')], 'Source':[],
            'Status':[], Description:[], 'Bandwidth/Baud':[]}

    myDict['Frequency'] = myDict['Frequency'] + ['None']
    myDict['Description'] = myDict['Description'] + ['None']
    myDict['Status'] = myDict['Status'] + ['None']
    myDict['Bandwidth/Baud'] = myDict['Bandwidth/Baud'] + ['None']
    myDict['Source'] = myDict['Source'] + ['UCS']


    return myDict

if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
