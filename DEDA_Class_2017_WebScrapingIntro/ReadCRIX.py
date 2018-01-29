"""
Description:
 - A simple demo to retrieve CRIX data and plot

Usage: Executing this whole file in your IDE or from Terminal or executing line by line in iPython.

Author: Junjie Hu, hujunjie@hu-berlin.de
Last modified date: 19-11-2017
"""

import requests
import json
import pandas as pd

url = 'http://crix.hu-berlin.de/data/crix.json'
r = requests.get(url)

content = r.content

js_content = json.loads(content)
for item in js_content:
    print(item)

data_raw = pd.DataFrame(js_content)
data_raw.set_index(keys='date', inplace=True)

data_raw.plot()
