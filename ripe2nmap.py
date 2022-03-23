#!/usr/bin/env python

import argparse
import netaddr
import json
import requests
import pprint
import re
import xml.etree.ElementTree as ET  

parser = argparse.ArgumentParser(description='Search RIPE database')
parser.add_argument('search_term', help='Search term used to search the RIPE database. Eg: facebook')
args = parser.parse_args()
pp = pprint.PrettyPrinter(indent=4)

simpleregex = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";
nogeenregex = "\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.\d{1,3} - [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.\d{1,3}\b"


# Search the RIPE database
# There is an issue with RIPE. When making a request and including
# the type-filter inetnum, the JSON response also includes other types.
request = requests.get('https://apps.db.ripe.net/db-web-ui/api/rest/fulltextsearch/select', params={
     'facet': 'true', 
     'format': ' xml',
      'hl': 'true', 
      'q': '('+args.search_term+')',
      'start': '0',
       'wt': 'json'
})
# answer = json.loads(request.text)
doc1 = ET.parse(request.text)
root = doc1.getroot()
for element in root.findall("strs"):
    iprange = element.find("lookup-key").text
    print (iprange)

# pp.pprint (json)

# Filter any object that doesn't have the type 'inetnum'
# ranges = [x['primary-key']['attribute'][0]['value']  for x in json['docs']['doc'] \
#        if x['object-type'] == 'inetnum']
# ranges = [x['lookup-key']['value'] for x in json if x['object-type'] == 'inetnum']

newJson = dict()
for (name, value) in answer.items():
    ip = re.findall(nogeenregex,str(value))
    print (ip)
    # if value == 'lookup-key':
    # newJson[key] = value

# pp.pprint (newJson)

# Turn the IP range string into CIDR
# cidrs = [];
# for _range in ranges:
    # _range = _range.split(' - ');
    # cidrs.append(netaddr.iprange_to_cidrs(_range[0], _range[1]))
# 
# Print the CIDR's
# for cidr in cidrs:
    # print (str(cidr[0]))
