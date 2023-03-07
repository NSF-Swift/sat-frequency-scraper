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
    amsat = amsat.iloc[:-48]

    #convert to dictionary
    amsat_dict = amsat.to_dict('list')

    return amsat_dict

if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
