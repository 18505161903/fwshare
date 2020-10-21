# encoding: utf-8
import pymongo,json
import pandas as pd
from pandas import Series,DataFrame
import future
from scipy.stats import pearsonr

import copy
from datetime import datetime, date, timedelta


pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

start = "20190529"
client = pymongo.MongoClient('localhost', 27017)
futures = client.futures
unit = futures.unit
position = futures.position
market = futures.market
positions = futures.positions
market = DataFrame(list(position.find({'date': {'$gte': start}})))





# sort_dict= sorted(market['volume'].items(),key=lambda X:X[1])


# market = market.sort_values( ascending=False, by=['variety','date','open_interest'])
# market = market.groupby(['date','variety']).head(2)

# market = market.groupby(['date','variety'])['close'].head(2)
# market = market.groupby(['date','variety'])["open_interest"].sum()
print(market)
