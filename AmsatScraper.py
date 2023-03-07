import pandas as pd
import requests

def Scraper():
    """
    Downloads an excel spreadsheet of amateur radio satellites 
    monitored by AMSAT-UK.
    """

    amsat_url = "http://www.ne.jp/asahi/hamradio/je9pel/satslist.xls"
    
    #request access to the url.
    r = requests.get(amsat_url, allow_redirects=True)

    if (r.status_code == 200):
        print('Request successful, converting to dataframe...')
    elif (r.status_code == 404):
        print('Error 404: Unsuccessful request, using prexisting dataframe...')

    #download and write contents onto the directory where script is saved.
    #XXX need to find way to read contents without having to download spreadsheet and waste storage.
    #Otherwise, need to create a directory for storing spreadsheets.
    open('amsat_data.xlsx', 'wb').write(r.content)
    
    #read spreadsheet and drop header
    amsat_xl = pd.read_excel('amsat_data.xlsx', skiprows=10)
    
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
