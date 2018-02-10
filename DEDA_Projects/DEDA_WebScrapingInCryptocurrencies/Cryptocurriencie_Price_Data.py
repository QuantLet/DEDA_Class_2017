
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:54:54 2017

@author: Alex
"""
import os

os.chdir("C:\\Users\\Tomas\\Desktop\\Crypto_Project")
path_direct = os.getcwd()

'''
packages plotly and quandl might need to be installed first
'''

import quandl
import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import datetime 


  
import quandl

#Define a function to pull the data from one exchange:
def crypto_data(chart_exchange):
    #Download and cache Quandl dataseries
    path = '{}.csv'.format(chart_exchange).replace('/','-')
    df = quandl.get(chart_exchange, returns='pandas')
    df.to_csv(path)
    return df  

df_kraken = crypto_data('BCHARTS/KRAKENUSD')



#First chart of Bitcoin timeseries from Bitstamp:
kraken_single = go.Scatter(x=df_kraken.index,
                           y=df_kraken['Weighted Price'],
                           name = 'kraken',
                           line = dict(color = '#30BEHF'))
py.plot([kraken_single],filename='btc_USD_Kraken.html')


# Pull pricing data for more BTC exchanges and safe them in a dictionary
exchanges = ['COINBASE','BITSTAMP','ITBIT']

exchange_data = {}

exchange_data['KRAKEN'] = df_kraken

for exchange in exchanges:
    exchange_code = 'BCHARTS/{}USD'.format(exchange)
    btc_df = crypto_data(exchange_code)
    exchange_data[exchange] = btc_df
    
#Merch into one single dataframe   
    def combine_dataframes(dataframes, labels, col):
        btc_dict={}
        for index in range(len(dataframes)):
            btc_dict[labels[index]] = dataframes[index][col]
            
        return pd.DataFrame(btc_dict)

btc_usd_datasets = combine_dataframes(list(exchange_data.values()), list(exchange_data.keys()), 'Weighted Price')

#Plotting the results:
bitstamp = go.Scatter(
           x = btc_usd_datasets.index,
           y = btc_usd_datasets.BITSTAMP,
           name = 'bitstamp',
           line = dict(color = '#17BECF'),
           opacity = 0.8)
           
coinbase =go.Scatter(
          x = btc_usd_datasets.index,
          y = btc_usd_datasets.COINBASE,
          name = 'coinbase',
          line = dict(color =  '#18EFGH'),
          opacity = 0.8)

itbit  = go.Scatter(
          x = btc_usd_datasets.index,
          y = btc_usd_datasets.ITBIT,
          name = 'itbit',
          line = dict(color =  '#23HFTP'),
          opacity = 0.8)
          
kraken  = go.Scatter(
          x = btc_usd_datasets.index,
          y = btc_usd_datasets.KRAKEN,
          name = 'kraken',
          line = dict(color =  '#30BEHF'),
          opacity = 0.8)

data = [bitstamp,coinbase,kraken,itbit]
fig = dict(data=data)
py.plot(fig,filename = 'BTC_USD.html')

#Readjust the plot and drop values of 0
btc_usd_datasets.replace(0, np.nan, inplace=True)

py.plot(fig, filename = 'BTC_USD.html')

#Average over the weighted prices of all 4 exchanges and plot the result

btc_usd_datasets['avg_BTC_price'] = btc_usd_datasets.mean(axis = 1)

avg_btc_price = go.Scatter(x = btc_usd_datasets.index,
                           y = btc_usd_datasets.avg_BTC_price,
                           name = 'Average BTC_USD price',
                           line = dict(color =  '#14DETF'), opacity = 0.8)

py.plot([avg_btc_price], filename = 'Average_BTC_USD_price')

btc_price = btc_usd_datasets["avg_BTC_price"]

