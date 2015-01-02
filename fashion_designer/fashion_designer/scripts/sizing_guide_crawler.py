from bs4 import BeautifulSoup
import requests

gustin = "https://www.weargustin.com/fitguide"
hm = "http://www.hm.com/us/sizeguide/sizeguide_men"

req_gustin = requests.get(gustin)
req_hm = requests.get(hm)

data_gustin = req_gustin.text
data_hm = req_hm.text

# Scrap all the size charts from gustin
soup = BeautifulSoup(data_gustin)

for link in soup.find_all('h4'):
    if 'guide' in link.get_text():
        clothes_type = link.get_text()

for table in soup.find_all('table'):
    print dir(table.find_next_sibling())
    #print table.findChild('td').findChild('strong')
    #print table.findChild('th').get_text()



