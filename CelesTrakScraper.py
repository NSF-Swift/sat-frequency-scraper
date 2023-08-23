import numpy as np
import pandas as pd

def Scraper():

    celestrak_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=csv"

    celestrak_csv = pd.read_csv(celestrak_url)
    celestrak_df = celestrak_csv[["OBJECT_NAME", "MEAN_MOTION", "NORAD_CAT_ID"]]

    p = celestrak_df["MEAN_MOTION"]
    celestrak_df.loc[(p > 0) & (p <= 2), "ORBIT_TYPE"] = "GEO"
    celestrak_df.loc[(p > 2) & (p <= 15), "ORBIT_TYPE"] = "MEO"
    celestrak_df.loc[(p > 15), "ORBIT_TYPE"] = "LEO"

    trunc_df = celestrak_df.drop(["MEAN_MOTION"], axis=1)

    celestrak_dict = trunc_df.to_dict('list')

    myDict = {
            "ID":[str(x) for x in celestrak_dict.pop("NORAD_CAT_ID")],
            "Name":[str(x) for x in celestrak_dict.pop("OBJECT_NAME")],
            "Orbit":[str(x) for (x) in celestrak_dict.pop("ORBIT_TYPE")]
    }
    myDict["Frequency"] = ["None" for x in myDict["ID"]]
    myDict["Bandwidth/Baud"] = ["None" for x in myDict["ID"]]
    myDict["Status"] = ["Active" for x in myDict["ID"]]
    myDict["Description"] = ["None" for x in myDict["ID"]]
    myDict["Source"] = ["CelesTrak" for x in myDict["ID"]]

    return myDict

if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
