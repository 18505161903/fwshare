# encoding: utf-8
import pymongo,json
import pandas as pd
from pandas import Series,DataFrame
import csv
from scipy.stats import pearsonr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import time,datetime
# from datetime import datetime
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行


client = pymongo.MongoClient('localhost', 27017)
futures = client.futures
unit = futures.unit
main = futures.main
signal = futures.signal
lots = futures.lots

start='20110101'
# var='A'

unit = DataFrame(list(unit.find()))
main= DataFrame(list(main.find({'date': {'$gte': start}})))
lots = DataFrame(list(lots.find()))

unit=unit[['variety','unit','minPrice']]
lots = lots[['variety','lots']]
# del main['_id']
main['signal']=main.groupby('variety')['交易信号'].shift(1)
main=main.dropna()
del main['_id']
# print(main.head())
df=pd.merge(main,unit,on=['variety'])#.drop_duplicates()
df1=pd.merge(df,lots,on=['variety'])#.drop_duplicates()
df=df1
# print(all_h1)
df['盈亏计算']= df.apply(lambda x: x['change'] * x['signal'] * x['unit']*x['lots'],axis=1)#.drop_duplicates()
# 交易成本
df['交易成本'] = df.apply(lambda x: x['unit']*x['minPrice']*x['lots']*abs(x['signal']),axis=1)#.drop_duplicates()
df['净利润'] = df['盈亏计算'] -df['交易成本']
# print(all_h.head())
df= df.drop_duplicates()
df['pnl'] = df['净利润'].cumsum()
df.to_csv(r"e:\signal.csv", mode='a', encoding='ANSI', header=True)

# signal.insert(json.loads(df.T.to_json()).values())
# print(json.loads(df.T.to_json()).values())