"""
Description:
 - Scraping Wallstreet Journal RSS feedback, printing out news title and description.
 - Using the attributes and methods of class defined in file "ReadRSSClass.py" from this file.

Usage: Executing this whole file in your IDE or from Terminal.

Author:
 - Junjie Hu, hujunjie@hu-berlin.de
 - Cathy Chen
Last modified date: 19-11-2017
"""

import os
import sys

sys.path.append(os.getcwd() + '/DEDA_Class_2017_WebScrapingIntro/')
# add the module path to Python searching path
import ReadRSSClass as rrc

# ReadRSSClass is the file name of the module code


r = rrc.ReadRSS("http://www.wsj.com/xml/rss/3_7085.xml")
r2 = rrc.ReadRSS("http://www.wsj.com/xml/rss/3_7085.xml")

# Here we can print out the object's url in certain format
print(r)

# Here we use == to validate if two responses of two url are equal
if r == r2:
    print("Two urls are the same")
else:
    print("Two urls are not the same")
# Print out the titles
r.get_titles()
# Print out the descriptions
r.get_description()
