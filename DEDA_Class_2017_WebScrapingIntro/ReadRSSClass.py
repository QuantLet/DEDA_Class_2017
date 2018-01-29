"""
Description:
 - Putting ReadRSS.py code into class so that we can use attributes from external files.
 - Introducing magic method.

Usage: This file is not for execution, only for external using.

Author:
 - Junjie Hu, hujunjie@hu-berlin.de
 - Cathy Chen
Last modified date: 19-11-2017
"""

import feedparser


class ReadRSS(object):
    # There are some methods with name surrounded by double underscore called "magic method"
    # Further more see: https://www.python-course.eu/python3_magic_methods.php
    def __init__(self, url):
        self.url = url
        self.response = feedparser.parse(self.url)

    def __eq__(self, other):
        # __eq__() is a magic method that enables comparison two object with ==
        if self.url == other.url:
            return True
        else:
            return False

    def __repr__(self):
        # __repr__() is a magic method that enables customization default printed format
        return "The website url is: " + self.url

    def get_titles(self):
        titles = []
        for item in self.response["entries"]:
            titles.append(item["title"])
        print("\nTITLES:\n")
        print('\n'.join(titles))
        return titles

    def get_description(self):
        scripts = []
        for item in self.response["entries"]:
            scripts.append(item["description"])
        print("\nDESCRIPTIONS:\n")
        print('\n'.join(scripts))
        return scripts
