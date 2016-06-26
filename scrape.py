import urllib
import json
import re
from bs4 import BeautifulSoup

urls = {"RiverView" : "https://www.irvinecompanyapartments.com/communities/river-view/prices-and-floorplans",
        "CrescentVillage" : "https://www.irvinecompanyapartments.com/communities/crescent-village/prices-and-floorplans",
        "NorthPark" : "https://www.irvinecompanyapartments.com/communities/north-park/prices-and-floorplans",}

for name, url in urls.iteritems():
    print "\n", name
    web = urllib.urlopen(url)
    pattern = re.compile('var FloorPlanData = (.*?);')

    soup = BeautifulSoup(web.read(), "lxml")
    scripts = soup.find_all('script')
    json_data = None
    for script in scripts:
       if(pattern.match(str(script.string))):
           data = pattern.match(script.string)
           json_data = json.loads(data.groups()[0])

    fields = ['PlanName', 'SquareFeet', 'MinimumRent', 'MaximumRent']

    for plan in json_data:
        if plan['PlanType'] == 'Two Bedrooms' and plan['AvailableUnits'] is not False:
            print ""
            for field in fields:
                print field, ':', plan[field]
