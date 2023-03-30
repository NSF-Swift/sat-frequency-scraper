import os
import time
import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def Scraper():
    """
    Automates a download of OSCAR satellite data via ChromeDriver.
    If run as an executable, data is presented as a DataFrame, otherwise it is presented as a dictionary.
    """

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    options.page_load_strategy = 'none'

    # returns the path web driver downloaded
    chrome_path = ChromeDriverManager().install()
    chrome_service = ChromeService(chrome_path)

    # pass the defined options and service objects to initialize the web driver
    driver = webdriver.Chrome(options=options, service=chrome_service)

    url = "https://space.oscar.wmo.int/satellitefrequencies"

    driver.get(url)
    driver.implicitly_wait(5)

    # close pop up tab
    driver.find_element(By.XPATH, '/html/body/div[7]/div[1]/button').click()

    # download OSCAR files
    for i in range(1,4):
        driver.execute_script(f'toggleBox({i});')
        driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[{i+1}]/div/form/button').click()
        time.sleep(2)

    # generate OSCAR DataFrames
    oscarXL = []
    for file in os.listdir():
        if (file[:7] == 'Oscar -'):
            oscarXL += [file]

    # for debugging
    # print(oscarXL)

    mw_xl = pd.DataFrame(pd.read_excel(oscarXL[0]))
    mw_df = mw_xl[['Id', 'Satellite', 'Frequency (GHz)', 'Bandwidth (MHz)', 'Comment']].rename(
                columns={'Frequency (GHz)': 'Frequency (MHz)', 'Bandwidth (MHz)': 'Bandwidth (kHz)'}
            )
    gs_xl = pd.DataFrame(pd.read_excel(oscarXL[1]))
    gs_df = gs_xl[['Id', 'Satellite', 'Frequency (MHz)', 'Bandwidth (kHz)', 'Comment']]

    sat_xl = pd.DataFrame(pd.read_excel(oscarXL[2]))
    sat_df = sat_xl[['Id', 'Satellite', 'Frequency (MHz)', 'Bandwidth (kHz)', 'Comment']]

    oscar_df = pd.concat([mw_df, gs_df, sat_df])

    # generate OSCAR dictionary
    sat_dict = oscar_df.to_dict('list')

    myDict = {
        'ID':[str(x) for x in sat_dict.pop('Id')],
        'Name':[str(x) for x in sat_dict.pop('Satellite')],
        'Frequency':[str(x) for x in sat_dict.pop('Frequency (MHz)')],
        'Bandwidth/Baud':[str(x) for x in sat_dict.pop('Bandwidth (kHz)')],
        'Description':[str(x) for x in sat_dict.pop('Comment')]
        }

    myDict['Status'] = ['None' for x in myDict['Name']]
    myDict['Source'] = ['Oscar' for x in myDict['Name']]

    # remove units from dictionary
    res_ghz = []
    res_mhz = []
    for each in myDict['Frequency']:
        ghz = "GHz"
        mhz = "MHz"
        if each.endswith(ghz):
            res_ghz.append(each.replace(ghz,'').strip())
        else:
            res_mhz.append(each.replace(mhz,'').strip())
                            
    # turn frenquency ranges into center frequencies
    for index in range(len(res_ghz)):
        each = res_ghz[index]
        if ('-' in each):
            indFreqs = [float(x.strip()) for x in each.split('-')]
            newF = str(np.average(indFreqs))
            res_ghz[index] = newF
                                                                                                            
    for index in range(len(res_mhz)):
        each = res_mhz[index]
        if ('-' in each):
            indFreqs = [float(x.strip()) for x in each.split('-')]
            newF = str(np.average(indFreqs))
            res_mhz[index] = newF
    
    # convert Ghz entries into MHz    
    res_ghz = [str(1000*float(x)) for x in res_ghz]

    myDict['Frequency'] = res_ghz + res_mhz

    # delete downloaded files
    for i in range(len(oscarXL)):
        os.remove(oscarXL[i])
    
    # close driver session
    driver.quit()

    return myDict

if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
