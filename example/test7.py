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
signal = futures.position
positionSignal =futures.positionSignal
lsPositionSignal =futures.lsPositionSignal
# # 查询数据
# mydict = {"long_party_name":None }
# x = signal.find(mydict)
# for i in x:
#     positionSignal.insert_one((i))

date = '20150101'
df = DataFrame(list(positionSignal.find({'date':{'$gte':date}})))
print(df.head(5))
df['signal'] = df.apply(lambda x: 1 if x['long_openIntr_chg']>0 and x['short_openIntr_chg']<0  else -1 if x['long_openIntr_chg']<0 and x['short_openIntr_chg']>0 else 0 ,axis=1)
del df["_id"]
lsPositionSignal.insert_many(json.loads(df.T.to_json()).values())
print(json.loads(df.T.to_json()).values())