import os
import time
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
    driver.implicitly_wait(5)

    url = "https://space.oscar.wmo.int/satellitefrequencies"

    driver.get(url)
    time.sleep(1) # time delay ensures that the webpage is fully loaded

    # close pop up tab
    nr_button = driver.find_element(By.XPATH, '/html/body/div[7]/div[1]/button')
    nr_button.click()

    # expand table and click export button
    driver.execute_script('toggleBox(1);')  # expand the menu
    ex_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/form/button')
    ex_button.click()

    # allow time for download to occur
    time.sleep(5)

    # generate OSCAR DataFrame
    oscarXL = []
    for file in os.listdir():
        if (file[:7] == 'Oscar -'):
            oscarXL += [file]

    oscar_df = pd.DataFrame(pd.read_excel(oscarXL[0])).drop([
        'Space Agency',
        'Launch ',
        'Eol',
        'Service',
        'Direction',
        'Emission',
        'Polarisation',
        'Data rate',
        'D/A'
        ],
        axis=1
    )

    # generate OSCAR dictionary
    oscar_dict = oscar_df.to_dict('list')

    myDict = {
        'ID':[str(x) for x in oscar_dict.pop('Id')],
        'Name':[str(x) for x in oscar_dict.pop('Satellite')],
        'Frequency':[str(x) for x in oscar_dict.pop('Frequency (MHz)')],
        'Bandwidth/Baud':[str(x) for x in oscar_dict.pop('Bandwidth (kHz)')],
        'Description':[str(x) for x in oscar_dict.pop('Comment')]
        }

    myDict['Status'] = ['None' for x in myDict['Name']]
    myDict['Source'] = ['Oscar' for x in myDict['Name']]
    newF = []
    for each in myDict['Frequency']:
            newF += [each.replace('MHz','').strip()]
            myDict['Frequency'] = newF

    # delete downloaded file
    os.remove(oscarXL[0])

    return myDict

if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
