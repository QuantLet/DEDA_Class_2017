"""
Description:
 - A simple demo to get json data from website by using json module

Usage: Executing this whole file in your IDE or from Terminal or executing line by line in iPython.

Author:
 - Junjie Hu, hujunjie@hu-berlin.de
 - Cathy Chen
Last modified date: 19-11-2017
"""

import requests
import json
import pprint

response = requests.get("https://data.ntpc.gov.tw/api/datasets/71CD1490-A2DF-4198-BEF1-318479775E8A/json/preview")
content = response.content
json_tree = json.loads(content)
pprint.pprint(json_tree)

for bike_rent_records in json_tree["result"]["records"]:
    leftRatio = float(bike_rent_records["sbi"]) / float(bike_rent_records["tot"]) * 100
    print("ID:{0} Left:{2:0.1f}% Name:{1}".format(bike_rent_records["sno"], bike_rent_records["aren"], leftRatio))
