
[<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/banner.png" width="888" alt="Visit QuantNet">](http://quantlet.de/)

## [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/qloqo.png" alt="Visit QuantNet">](http://quantlet.de/) **Digital Economy and Decision Analytics** [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/QN2.png" width="60" alt="Visit QuantNet 2.0">](http://quantlet.de/)

```yaml

Name of Quantlet : DEDA_Class_2017_Python_Introduction

Published in : Digital Economy and Decision Analytics

Description : Introduce basic syntax for operations, numeric and string, and basic data structure, list, tuple, set and dict in Python

Keywords :
- Python
- Teaching
- Data Science
- Economy
- Decision

Author : Junjie Hu

```

### Python Installation Guide
You can choose downloading python from the [Official Website](https://www.python.org/):

For Mac user, You can also download it from the terminal using the [homebrew](https://brew.sh/).

After installation of `homebrew`, type in the terminal:

`brew install python3`



### Python Code:
```python


"""
Python Basic Syntax and Data Structure Introduction
"""

"""
numeric operation
"""
"""
try basic operations:
+, -, *, /, %, **, //
"""

a = 5
b = 3
a *= 2  # 10
round(a / b, 4)  # 3.3333

c = '10'
d = '20'
e = c + d  # '1020'
f = int(c) + int(d)  # 30

"""
try comparision operations:
==, <, <=, >, >=, !=
"""

"""
string
"""
"""
String is a basic type in python, it's common used and very powerful
"""

welcome_list = ['Welcome', 'to', 'Python', 'World.', 'It\'s', 'Amazing']
# using back slash to escape the single quote.

# using for loop to iterate all elements in the list.
for word in welcome_list:
    print(word)

# a string is also an object, using the join method to connect all the words in the list.
welcome_sentence = ' '.join(welcome_list)

# slicing string by indices.
welcome_sliced = welcome_sentence[0:10]
# try changing the indices to negative.

# see other methods of string object, like:
welcome_upper_case = welcome_sentence.upper()
# by using dir() function, or help() function
dir(str)
# or a str instance
dir(welcome_upper_case)
# likewise,
help(str)

# formatting string
greeting = 'Hallo'
name = 'Jon'
# using format method
welcome_jon = '{}, {}. '.format(greeting, name.upper()) + welcome_sentence
# using f string, you can write variable name into brackets, directly.
welcome_jon_f = f'{greeting}, {name.upper()}. ' + welcome_sentence

"""
tuple and set
"""
"""
tuple and set are two basic structures with different features to list.
"""

# tuple is very alike list, but tuple is immutable
person_list = ['Jon Dow', '06-04-2000', 'Male', 'U.S.A']
person_tuple = ('Jon Dow', '06-04-2000', 'Male', 'U.S.A')
person_list[0] = 'Allan Lee'  # ['Allan Lee', '06-04-2000', 'Male', 'U.S.A']
person_tuple[0] = 'Allan Lee'  # tuple' object does not support item assignment

# set
countries_1 = {'China', 'Korea', 'Japan', 'Turkey', 'Singapore', 'Russia', 'Japan'}
countries_2 = {'UK', 'Germany', 'France', 'Spain', 'Italy', 'Russia', 'Turkey'}

print(countries_1)  # sets will drop duplicated elements automatically
count_inter = countries_1.intersection(countries_2)  # {'Russia', 'Turkey'}
count_1_diff = countries_1.difference(countries_2)  # {'China', 'Japan', 'Korea', 'Singapore'}
count_2_diff = countries_2.difference(countries_1)  # {'France', 'Germany', 'Italy', 'Spain', 'UK'}
countries_new = countries_1.union(countries_2)  # merge two sets into 1 and without duplicates

"""
list
"""
"""
Using list makes Python code simple.
"""

natr_language = ['English', 'German', 'Chinese']
prog_language = ['C++', 'Java', 'C#']

# how many elements in a list?
len(natr_language)  # 3
# how many elements in a string?
len(natr_language[0])  # 7

# adding elements into the list
# append() allows you to add 1 element at the end of the list
natr_language.append('Spanish')  # ['English', 'German', 'Chinese', 'Spanish']

# insert() allows you to add 1 element at arbitrary place
prog_language.insert(0, 'Python')  # ['Python', 'C++', 'Java', 'C#']

# extend() allows you to add multiple elements at the end of the list
python = ['python 2.7', 'python 3.6']
prog_language.append(python)  # ['Python', 'C++', 'Java', 'C#', ['python 2.7', 'python 3.6']]
more_language = ['Japanese', 'Korean']
natr_language.extend(more_language)  # ['English', 'German', 'Chinese', 'Spanish', 'Japanese', 'Korean']

# remove elements
prog_language.remove(python)  # ['Python', 'C++', 'Java', 'C#']
natr_language.pop(-1)  # 'Korean' pops out. ['English', 'German', 'Chinese', 'Spanish', 'Japanese']
del prog_language[-1]  # ['Python', 'C++', 'Java']

# reorder in list
numbers = [43, 11, 32, 95, 22]
numbers.reverse()  # [22, 95, 32, 11, 43]
numbers.sort()  # [11, 22, 32, 43, 95]
numbers.sort(reverse=True)  # [95, 43, 32, 22, 11]
sorted_number = sorted(numbers)  # sorted function can return a new list instead of altering the original list

# basic search in list
min_num = min(numbers)  # 11
max_num = max(numbers)  # 95
sum_num = sum(numbers)  # 203
index_num = numbers.index(32)  # 2

# iterate in list
for lang in prog_language:
    print(lang)
# iterate in list with index
for num, lang in enumerate(natr_language):
    print(f'{num}. {lang}')

# list to string
natr_language_str = ', '.join(natr_language)  # 'Spanish, Japanese, German, English, Chinese'
natr_language_new = natr_language_str.split(', ')  # ['Spanish', 'Japanese', 'German', 'English', 'Chinese']

# looping in the list. The basic syntax is:
# [func(ele) for func(ele) in a_list if func(ele)]
# For example:
people = [language + ' People' for language in natr_language_new if language.endswith('ese')]
# format number in list to 2 digit
num_seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
num_seq_db = [format(num, '02d') for num in num_seq]

"""
Dictionary
"""
"""
Like a real dictionary, dict type is form by 2 parts, a unique key and values for a key.
"""

# initial a dict
profile = {'name': 'Anna', 'birth': '10-05-2000', 'gender': 'female', 'height': 1.70}

# find the value by using the key
print(profile['name'])  # 'Anna'

# get all the keys and put into a list
keys = list(profile.keys())  # ['name', 'birth', 'gender', 'height']
# get all values and put into a list
values = list(profile.values())  # ['Anna', '10-05-2000', 'female', 1.7]
# get all key-value pairs and put into a list
key_value = list(profile.items())

# add a key with value
profile['weight'] = 55
# change value of a key
profile['name'] = 'Yoki'
# alter multiple keys and values at a time
profile.update({'birth': '01-10-2001', 'tel': '123-312'})

# loop with key and vlaue
for key, value in profile.items():
    print(f'{key}: {value}')


```

