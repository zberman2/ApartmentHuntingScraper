# -*- coding: utf-8 -*-

import time
import urllib
import json
import re
from bs4 import BeautifulSoup
import webbrowser

def approve_plan(plan_json):
    """
    This function ensures that only floor plans satisfy the following criteria:
        2 Bedrooms
        2 Bathrooms
        Unit is Available
        MinimumRent is less than or equal to $3500

    'plan_json' : JSON object containing a single Floor Plan
    Return True if plan_json satisfies the above criteria
    """
    return plan['Bedrooms'] == 2 and \
           plan['Bathrooms'] == "2" and \
           plan['AvailableUnits'] is not False and \
           plan['MinimumRent'] <= 3500

urls = {"RiverView" : "https://www.irvinecompanyapartments.com/communities/river-view/prices-and-floorplans",
        "CrescentVillage" : "https://www.irvinecompanyapartments.com/communities/crescent-village/prices-and-floorplans",
        "NorthPark" : "https://www.irvinecompanyapartments.com/communities/north-park/prices-and-floorplans",}

print "\nDisplaying Irving Company Apartments floor plan information..."
print "\nAll floor plans must satisfy the following criteria:"
print "\n\tAvailable == True\n\t2 Bedrooms\n\t2 Bathrooms\n\tMinimumRent <= 3500"

f = open('output.txt', 'w')

for name, url in urls.iteritems():
    web = urllib.urlopen(url)
    # FloorPlanData houses the JSON information we want
    pattern = re.compile('var FloorPlanData = (.*?);')

    soup = BeautifulSoup(web.read(), "lxml")
    scripts = soup.find_all('script')
    json_data = None
    for script in scripts: # cycle through the script tags in the page source
       if(pattern.match(str(script.string))):
           data = pattern.match(script.string)
           json_data = json.loads(data.groups()[0])

    fields = ['PlanName', 'MinimumRent', 'MaximumRent', 'SquareFeet']

    name_string = "\n" + name
    print name_string # print apartment complex name (e.g. "RiverView")
    f.write(name_string + "\n")

    for plan in json_data:
        if approve_plan(plan):
            print ""
            f.write("\n")
            for field in fields:
                field_string = field + ': ' + str(plan[field])
                print field_string
                f.write(field_string + "\n")

from subprocess import call
call('git add output.txt', shell = True)
call('git commit -a "committing new output file"', shell = True)
call('git push origin master', shell = True)

print "\nWould you like to open the 3 urls in your web browser? (y/n)"
response = raw_input().lower()
if response == 'y':
    print "\nComing right up!\n"
    for name, url in urls.iteritems():
        webbrowser.open_new_tab(url)
        time.sleep(1)
elif response == 'n':
    print "\nHave a nice day!\n"
else:
    text = "\nヽ(ಠ_ಠ)ノ What about (y/n) don't you understand!! (╯°□°）╯︵ ┻━┻\n".decode('utf-8')
    print text.encode('utf-8')
