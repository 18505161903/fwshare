# encoding: utf-8

import pandas as pd
from pandas import *
import datetime
import json
from pymongo import MongoClient

pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

client = MongoClient('localhost', 27017)
db = client.futures
indexMarket = db.indexMarket

indexMarket = DataFrame(list(indexMarket.find()))

df = indexMarket[['date', 'variety', 'set_high', 'set_low']]

for i in set(indexMarket['variety']):
    #     # print(i)
    try:
        df2 = df[df['variety'] == i]
        # print(df2)

        max = df2.rolling(window=60, on='variety').max().dropna()  # ,min_periods=1
        # print(max.tail(5))
        min = df2.rolling(window=60, on='variety').min().dropna()
        #     # print(min.tail(5))
        hb = pd.merge(max, min, on=['date', 'variety'], how='outer').fillna(method='ffill')
        # print(hb)

        data=hb[['date','variety','set_high_x','set_low_y']]
        # print(data.head(5))

        # 涨幅
        data['gains'] = round((data['set_high_x'] / data['set_low_y'] - 1) * 100, 2)
        # 跌幅
        data['lesses'] = round((1 - data['set_low_y'] / data['set_high_x']) * 100, 2)
        data['variety']='jd'
        print(data)


    except:
        pass
    continue

# print('完成')
# data['variety']='jd'

# data['gains']=round(data.apply(lambda x: (x['set_high_x'] / x['set_low_y']-1)*100, axis=1), 2)
# 跌幅
# data['losses'] = round(data.apply(lambda x: (1 - x['set_low_y'] / x['set_high_x']) * 100, axis=1), 2)