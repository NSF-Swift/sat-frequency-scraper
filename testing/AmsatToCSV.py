import sys
sys.path.append('../')
from AmsatScraper import Scraper
import pandas as pd
import numpy as np

myFrame = pd.DataFrame.from_dict(Scraper())
myFrame.to_csv('AmsatDB.csv', index=True)
