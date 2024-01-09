import io
import numpy as np
import pandas as pd
from spacetrack import SpaceTrackClient

def Scraper():

    st = SpaceTrackClient(identity="crforrester@berkeley.edu", password="b*4PZCPZj*Q8pN6")

    data = st.satcat(object_type="payload", current="Y", decay=None, orderby="norad_cat_id", format="csv")
    spacetrack_df = pd.read_csv(io.StringIO(data))
    trunc_df = spacetrack_df[["NORAD_CAT_ID", "SATNAME", "COMMENT", "PERIOD"]]

    spacetrack_dict = trunc_df.to_dict("list")
    periods = np.array([float(x) for x in spacetrack_dict.pop("PERIOD")])
    mean_motion = (60*24)/periods
    orbits = []

    for mot in mean_motion:
        if ((mot >= 0) and (mot < 2)):
            orbits += ['GEO']
        elif ((mot >= 2) and (mot <= 15)):
            orbits += ['MEO']
        elif (mot >= 15):
            orbits += ['LEO']
        else:
            orbits += ['None']
    #celestrak_df.loc[(p >= 0) & (p < 2), "ORBIT_TYPE"] = "GEO"
    #celestrak_df.loc[(p >= 2) & (p < 15), "ORBIT_TYPE"] = "MEO"
    #celestrak_df.loc[(p >= 15), "ORBIT_TYPE"] = "LEO"


    myDict = {
            "ID":[str(x) for x in spacetrack_dict.pop("NORAD_CAT_ID")],
            "Name":[str(x) for x in spacetrack_dict.pop("SATNAME")],
            "Description":[str(x) for x in spacetrack_dict.pop("COMMENT")],
            "Orbit":orbits
    }
    myDict["Frequency"] = ["None" for x in myDict["ID"]]
    myDict["Bandwidth/Baud"] = ["None" for x in myDict["ID"]]
    myDict["Status"] = ["Active" for x in myDict["ID"]]
    myDict["Source"] = ["Space-Track" for x in myDict["ID"]]

    return myDict

if __name__ == "__main__":
    myFrame = pd.DataFrame.from_dict(Scraper())
    print(myFrame)
