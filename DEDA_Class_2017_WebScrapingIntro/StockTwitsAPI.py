"""
Description:
 - This class is for API StockTwits
 - Usage for searching and retrieving

Usage: Using this class from external files

Author: Roméo Després <romeo.despres@ens-rennes.fr>
Last modified date: 27-11-2017
"""


import requests

class StockTwitsApi:

  def __init__(self):
    self.base = "https://api.stocktwits.com/api/2/"
    self.token = ""

  def login(self, token):
    self.token = token
    return(self)

  def search(self, mode=None, **kwargs):

    """ mode can have value None, "users" or "symbols"."""

    url = self.base + "search{}.json".format("" if mode is None else "/" + mode)
    if self.token != "":
      kwargs.update({"access_token": self.token})
    result = requests.get(url, params=kwargs)
    return(result)

  def stream_symbol(self, id, **kwargs):
    url = self.base + "streams/symbol/{}.json".format(id)
    if self.token != "":
      kwargs.update({"access_token": self.token})
    result = requests.get(url, params=kwargs)
    return(result)
