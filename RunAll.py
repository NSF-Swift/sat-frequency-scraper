import mechanicalsoup
import requests
import pandas as pd

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

compDict = {'ID':IDs, 'Name':names, 'Frequency [MHz]':freqs, 'Status':stats, 'Description':descs}

myFrame = pd.DataFrame.from_dict(compDict)
myFrame.to_csv('SatList.csv', index=False)
