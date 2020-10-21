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
lots = futures.lots
signal = futures.indexMarket
unit = futures.unit


market = DataFrame(list(signal.find({'date': {'$gte': '20190601'}})))
market=market.duplicated()
# print(market)

# # 查询数据
mydict = {"date": "20190801"}
x = signal.find_one(mydict)
print(x)

# # 添加数据
# mydict = {"variety": "AAAA","lots":5}
# lots.insert_one(mydict)

# # 删除数据
# myquery = {"variety": "IF"}
# unit.delete_one(myquery)

# myquery = {"variety": "IF"}
# unit.delete_one(myquery)

# 修改数据
# myquery = {"variety": "IF","lots":5}
# newvalues = {"$set": {"variety": "IF","lots":1}}
# lots.update_one(myquery, newvalues)

