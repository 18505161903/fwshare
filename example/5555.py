# encoding: utf-8

import pandas as pd
from pandas import *
import datetime
import json
from pymongo import MongoClient
from collections import defaultdict

pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

client = MongoClient('localhost', 27017)
db = client.futures
indexMarket = db.indexMarket
peak = db.peak
unit=db.unit

start='20190601'
# var='JD'

indexMarket = DataFrame(list(indexMarket.find({'date': {'$gte': start}})))

unit = DataFrame(list(unit.find()))
dd=unit['variety']