import urllib
import json
import re
from bs4 import BeautifulSoup

web = urllib.urlopen("https://www.irvinecompanyapartments.com/communities/river-view/prices-and-floorplans")
pattern = re.compile('var FloorPlanData = (.*?);')

soup = BeautifulSoup(web.read(), "lxml")
scripts = soup.find_all('script')
json_data = None
for script in scripts:
   if(pattern.match(str(script.string))):
       data = pattern.match(script.string)
       json_data = json.loads(data.groups()[0])

print json_data[0]['Id']
