#!/usr/bin/env python
# coding=utf-8
'''
Author: John
Email: johnjim0816@gmail.com
Date: 2020-12-13 19:47:25
LastEditor: John
LastEditTime: 2020-12-13 19:54:43
Discription: 
Environment: 
'''


import pandas as pd
import requests
import io
url='https://raw.githubusercontent.com/transhi/Pokemon_dash/master/data/Pokedex_Ver6_with_power.csv'

df=pd.read_csv(url)
print(df)