import pandas as pd
import requests

def Scraper():
    """
    Downloads an excel spreadsheet of space stations authorized by the FCC 
    and converts it into a pandas dataframe.
    """

    fcc_url = "https://transition.fcc.gov/ib/sd/se/ssal.xlsx"

    #read spreadsheet and convert into dataframe
    fcc_xl = pd.read_excel(fcc_url)
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

    #convert to dictionary
    fcc_dict = fcc.to_dict('list')

    return fcc_dict

if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
