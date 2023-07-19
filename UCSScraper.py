import pandas as pd
import requests
import re
import numpy as np



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

    myDict = {'Friendly Name':friendly_names, 'Alternate Names':alternate_names,
            'Official Name':[str(x) for x in ucs_dict.pop('Current Official Name of Satellite')],
            'ID':[str(x) for x in ucs_dict.pop('NORAD Number')], 'Orbit Class':[str(x) for x in ucs_dict.pop('Class of Orbit')]}


    return myDict

if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
