"""
Description:
 - A simple demo to get XML data.

Author:
 - Cathy Chen
Last modified date: 5-11-2017
"""

import requests
import xml.dom.minidom

response = requests.get(
    "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Datasets/daily_treas_bill_rates.xml")
content = response.content
dataDOM = xml.dom.minidom.parseString(content)
response = requests.get(
    "https://news.google.com/news/rss/headlines/section/q/finance%20news/finance%20news?ned=us&hl=en")
