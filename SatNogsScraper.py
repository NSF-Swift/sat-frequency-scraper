import mechanicalsoup
import requests
import pandas as pd


def Scraper():
    """
    Returns dictionary consisting of ID, Name, Frequency, Status, and Description
    """
    url = 'https://db.satnogs.org/transmitters'
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(url)
    myRes = browser.get_current_page().find_all("tr")
    rowTag = myRes[1].contents[1]
    myDict = {'ID':[], 'Name':[], 'Frequency':[], 'Bandwidth/Baud':[], 'Status':[], 'Description':[]}
    for each in myRes[1:]:
        if (each.contents[1] == rowTag):
            strID = str(each.contents[5].contents[1].contents[0]).strip()
            strName = strID[strID.index('-') + 1:].strip()
            strNum = strID[:strID.index('-')].strip()
            strFreq = str(each.contents[11].contents[0])
            try:
                strFreq = str(float(strFreq)/1000000)
            except:
                pass
            strDesc = str(each.contents[9].contents[0])
            strStatus = str(each.contents[27].contents[0])
            strBaud = str(each.contents[23].contents[0]).strip()
            myDict['ID'] = myDict['ID'] + [strNum]
            myDict['Name'] = myDict['Name'] + [strName]
            myDict['Frequency'] = myDict['Frequency'] + [strFreq]
            myDict['Description'] = myDict['Description'] + [strDesc]
            myDict['Status'] = myDict['Status'] + [strStatus]
            myDict['Bandwidth/Baud'] = myDict['Bandwidth/Baud'] + [strBaud]
    return myDict





if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
