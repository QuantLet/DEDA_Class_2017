
[<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/banner.png" width="888" alt="Visit QuantNet">](http://quantlet.de/)

## [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/qloqo.png" alt="Visit QuantNet">](http://quantlet.de/) **Digital Economy and Decision Analytics** [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/QN2.png" width="60" alt="Visit QuantNet 2.0">](http://quantlet.de/)

```yaml

Name of Quantlet : DEDA_Class_2017_InputOutput
Published in : Digital Economy and Decision Analytics
Description : Introduce importing packages, reading and writing files, using pandas to read and write structured data.
Keywords : 
- Python
- Teaching
- import package
- pickle
- pandas
- csv
- json
Author : Junjie Hu

```

### Python Code:
```python

# -*- coding: utf-8 -*-


"""
Introduce the input and output in Python
"""

"""
Import packages
"""

# Using "import" can input packages (modules), .py files from defined paths
# 2 ways to import
import os
path_direct = os.getcwd()
os.chdir(path_direct + '/DEDA_Class_2017_InputOutput')
# os module allows you to connect with your operation system
# You can check, create, delete, rename your files and directories
# Hint: path.exists(), listdir(), mkdir(), makedirs(), remove(), removedirs(), rename(), walk()
# Give the package an alias
import numpy as np
np.power(2, 10)  # 1024

# Instead of importing whole package, import only 1 method in the package
from pandas import DataFrame
some_info = {'name': ['Alice', 'Bob', 'Clark', 'Douglas'],
            'age': [5, 10, 3, 22]}
df = DataFrame(some_info)


"""
Read and write file
"""

# Using build-in function, open(), to open the file and using close() to close the file
shakespeare = open('shakespeare.txt', 'r', encoding='utf-8')
for string in shakespeare:
    print(string)
shakespeare.close()

# In python, we usually use syntax "with open() as container_name" to load the content
# There are 3 basic containers here:
with open('shakespeare.txt', 'r') as shakespeare_read:
    # read(n) method will put n characters into a string
    shakespeare_string_10 = shakespeare_read.read(10)
    shakespeare_string = shakespeare_read.read()

with open('shakespeare.txt', 'r') as shakespeare_read:
    # readline() method will read one line once.
    print(shakespeare_read.readline(), end='*')
    print(shakespeare_read.readline(), end='*')
    print(shakespeare_read.readline(), end='*')

with open('shakespeare.txt', 'r') as shakespeare_read:
    # readlines() method will put content into a list, every line is a string in the list
    shakespeare_lines = shakespeare_read.readlines()
    print(shakespeare_lines)

for line in shakespeare_lines:
    print(line)

# Using pickle to serialize data, save as binary format
# Create a standard normal distribution data set
temp_data = np.random.normal(size=100000)
temp_data = list(temp_data)
import matplotlib.pyplot as plt
plt.hist(temp_data, 100)
import pickle
# If you are writing plain text, you can use 'w'
# If you want to save as binary format, you should use 'wb'
with open('temp.pkl', 'wb') as temp_file:
    pickle.dump(temp_data, temp_file)


"""
Input and output structured data
"""
import pandas as pd
# Pandas supports most of the common structured data formats
# The read_csv method can take more arguments to satisfy your need
# For example, you can specify the delimiter and decimal style
# further more see: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
apple_stock = pd.read_csv('AAPL.csv', index_col='date', parse_dates=True)
# Pandas will read files as DataFrame type
# This is a very powerful data structure that you can do almost everything to the data.
type(apple_stock)
# For example, easily slicing rows and selecting columns
apple_stock_2013 = apple_stock.loc[apple_stock.index.year == 2013, ['low', 'high', 'open', 'close', 'volume']]

# Save the new data as json format
apple_stock_2013.to_json('AAPL_2013.json')
apple_stock_2013.to_csv('test.csv')


```

