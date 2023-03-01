import mechanicalsoup
import requests
import pandas as pd
import numpy as np

### Import Scrapers
from RadioGuyScraper import Scraper as rgs
from SatNogsScraper import Scraper as sns

myDicts = [sns(), rgs()]

IDs, names, freqs, stats, descs = [], [], [], [], []
for each in myDicts:
    IDs += each['ID']
    names += each['Name']
    freqs += each['Frequency']
    stats += each['Status']
    descs += each['Description']

"""
Sort based off Names
"""

nameInds = np.argsort(np.array(names))
names = list(np.array(names)[nameInds])
IDs = list(np.array(IDs)[nameInds])
freqs = list(np.array(freqs)[nameInds])
stats = list(np.array(stats)[nameInds])
descs = list(np.array(descs)[nameInds])

compDict = {'ID':IDs, 'Name':names, 'Frequency [MHz]':freqs, 'Status':stats, 'Description':descs}

"""
index = 0
for each in names:
    if (freqs[index] in freqs[index + 1:]):
        print(each)
    index += 1

"""







myFrame = pd.DataFrame.from_dict(compDict)
#print(sorted(names))
myFrame.to_csv('SatList.csv', index=False)
