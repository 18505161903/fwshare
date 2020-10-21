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
yk=futures.yk

start='20190101'
# var='A'

unit = DataFrame(list(unit.find()))
main= DataFrame(list(main.find({'date': {'$gte': start}})))

unit1=unit[['variety','unit']]
# del main['_id']
main['昨日交易信号']=main.groupby('variety')['交易信号'].shift(1)
main=main.dropna()
del main['_id']
# print(main.head())
all_h=pd.merge(main,unit1,on=['variety'])#.drop_duplicates()
# print(all_h1)
all_h['盈亏计算']= all_h.apply(lambda x: x['change'] * x['昨日交易信号'] * x['unit'],axis=1)#.drop_duplicates()
# print(all_h.head())
all_h= all_h.drop_duplicates()
all_h['pnl'] = all_h['盈亏计算'].cumsum()
all_h.to_csv(r"e:\signal.csv", mode='a', encoding='ANSI', header=True)