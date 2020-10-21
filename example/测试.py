# encoding: utf-8
import datetime
import pandas as pd
from pandas import DataFrame
import json
from pymongo import MongoClient


pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

client = MongoClient('localhost', 27017)
db = client.futures3
position = db.position
date = "20190920"

#加载数据

position = DataFrame(list(position.find({'date': {'$gte': date}})))
position=position[position['variety']=='MA']
print(position.head(4))