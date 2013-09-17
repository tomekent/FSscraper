
def Scrape(IATA):
	import lxml.html
	import requests
	import os, sys, csv, optparse
	from lxml import etree
	from lxml import html
	from lxml.html.clean import clean_html
	from datetime import datetime, timedelta
	
	#airport = sys.argv[1]
	airport = IATA
	yest = datetime.today() - timedelta(days=1)
	date = '%02.f-%02.f-%02.f' %( yest.year, yest.month, yest.day)

		# Set the time periods to query
	queryTimes = ['3','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']

	outfile = 'Data/FSScrape_%s_%s.csv' %( airport, date)
	output = csv.writer(open(outfile, 'w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	#Add a few header to the urlrequest
	headers = {
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.65 Safari/537.36',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Host' : 'www.flightstats.com',
		'Connection' : 'keep-alive',
		'Accept-Language' : 'en-Us, en; q=0.8'
	}
	
	for idqt, qT in enumerate(queryTimes):
		page = requests.get('http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=%s&airportQueryDate=%s&airportQueryTime=%s&airportQueryType=0&queryNext=false&queryPrevious=false&sortField=3&airportToFilter=--+All+Airports+--&codeshareDisplay=0&airlineToFilter=--+All+Airlines+--' % (airport, date, qT), headers)
		tree = html.fromstring(page.text)
		tbl = tree.xpath('//td[@id="mainAreaLeftColumn"]/table/tr')

		print " -- Found %s rows for %s in QueryTime %.f" % (len(tbl), airport, idqt + 1)
		for r in tbl:
			# data = r.xpath("td")
			data = r
			try:  # in a try so we drop lines that don't have enough data
				line = list()
				line.append(airport)
				src = data[0].xpath("a")[0]
				if type(src.text) is str:
					line.append(src.text)
				else:
					line.append(src.text)
				
				x = data[1][0]
				if type(x.text) is str:
					line.append(x.text.replace('\n',''))
				else:
					line.append('')
						
				for idx, x in enumerate(data[3:9]):
					if idx in (1,2):
						if type(x.text) is str:
							oldtime = x.text.replace('\n','')
							newtime = datetime.strptime('%02.f-%02.f-%02.f' %( yest.year, yest.month, yest.day) + ' ' + oldtime,'%Y-%m-%d %H:%M %p')
							line.append('%02.f' % (newtime - datetime.utcfromtimestamp(0)).total_seconds())
						else:
							line.append('')
					if type(x.text) is str:
						line.append(x.text.replace('\n',''))
					else:
						line.append('')
					
				output.writerow(line)	
			except:
				pass
				
	return outfile
			
import os, sys, csv, optparse
from datetime import datetime, timedelta
import time

csvfile = sys.argv[1]
cr = csv.reader(open(csvfile,"rb"))
IATA = list()
for row in cr:
	IATA.append(row[0])
		
count = 0
for id, row in enumerate(IATA):   
	print 'Begining Scrape for %s, %02.f of %02.f' %( row, id + 1, len(IATA)) 
	outfile = Scrape(row) 
	print 'Scrape Complete for %s, \nData saved: %s' %( row, outfile)
	print 'Sleeping 1\n'
	time.sleep(1)
