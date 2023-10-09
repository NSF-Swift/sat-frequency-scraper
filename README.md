# satellite frequency scraper

install.sh can be run independently to install all prerequisites before running the main scraper or can be run as a Docker container with 
docker build -t satellite-scraper .
docker run -it satellite-scraper

RunAll.py may be used as an executable, i.e.:
python RunAll.py
which produces our complete satellite database in the form of a csv file SatList.csv

The function ScrapeAll() may also be imported from RunAll.py and returns a dictionary
of the satellite ID's, Names, Center Frequencies [MHz], Bandwidth[kHz]/Bauds, Status, and Descriptions

Google Documentation:
https://docs.google.com/document/d/15oGHv-g_fN-kdFUalYqRe3PEQc5fqNjRH-qsMR46SFs/edit?usp=sharing
