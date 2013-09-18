#			 README 			#
##    FLIGHT DELAY SCRAPER		##
##     Tom Kent 2013			##

***


Used to get data from FLightStats.com, namely the delay data.
Only get free access to non-historical data, ie the last 24 hours.


## Example Usage

* $ Python scrapeFS.py 'JFK' '2013-09-15'

* Takes the IATA of the airport and a date (will probably only work for the day before) by default it will do yesterdays date.

* Saves to a file called FSScrape_$IATA_CODE$.csv

