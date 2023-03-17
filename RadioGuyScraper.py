import mechanicalsoup
import requests
import pandas as pd

def Scraper():
    """
    Returns dictionary consisting of ID, Name, Frequency, Status, and Description
    """
    url = 'https://usradioguy.com/satellite-frequencies/'
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(url)
    myRes = browser.get_current_page().find_all("tr")

    myDict = {'ID':[], 'Name':[], 'Frequency':[], 'Status':[],
             'Bandwidth/Baud':[], 'Description':[]}

    for each in myRes[1:]:
        satName = str(each.contents[1].contents[0])
        ID = 'None'
        bw = str(each.contents[8].contents[0]).strip()
        FreqRaw = str(each.contents[7].contents[0]).strip()
        mInd = FreqRaw.index("M")
        Freq = FreqRaw[:mInd].strip()
        statRaw = str(each.contents[11].contents[0]).strip()
        if (statRaw == 'D'):
            stat = 'inactive'
        else:
            stat = 'active'
        Desc = str(each.contents[12].contents[0]).strip()
        myDict['ID'] = myDict['ID'] + [ID]
        myDict['Name'] = myDict['Name'] + [satName]
        myDict['Frequency'] = myDict['Frequency'] + [Freq]
        myDict['Status'] = myDict['Status'] + [stat]
        myDict['Bandwidth/Baud'] = myDict['Bandwidth/Baud'] + [bw]
        myDict['Description'] = myDict['Description'] + [Desc]
    return myDict





if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
