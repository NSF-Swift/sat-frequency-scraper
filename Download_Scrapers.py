import pandas as pd
import requests

def Fcc_Scraper():
    """
    Downloads an excel spreadsheet of space stations authorized by the FCC 
    and converts it into a pandas dataframe.
    """

    fcc_url = "https://transition.fcc.gov/ib/sd/se/ssal.xlsx"

    #request access to the url.
    r = requests.get(fcc_url, allow_redirects=True)

    if (r.status_code == 200):
        print('Request successful, converting to dataframe...')
    elif (r.status_code == 404):
        print('Error 404: Unsuccessful request, using prexisting dataframe...')
    
    #download and write contents onto the directory where script is saved.
    #XXX need to find way to read contents without having to download spreadsheet and waste storage.
    #Otherwise, need to create a directory for storing spreadsheets.
    open('fcc_data.xlsx', 'wb').write(r.content)
    
    #read spreadsheet and convert into dataframe
    fcc_xl = pd.read_excel('fcc_data.xlsx')
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

    pd.set_option('display.max_columns', 100)
    print(fcc)

def Amsat_Scraper():
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

    pd.set_option('display.max_columns', 100)
    print(amsat)

