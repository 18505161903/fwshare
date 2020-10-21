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
futures = client.futures2
market = futures.position



# market = DataFrame(list(market.find({'date': {'$gte': '20190601'}})))

# # 删除数据
begin = DataFrame(list(market.find({}).sort([('_id', -1)]).limit(1)))
print(begin.head())
begin = begin['date'][0]
print("lastdate: "+begin)







from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from datetime import datetime
import time
# dr=['2001-1-1','2030-1-1']
# d=pd.to_datetime(dr)
# d=pd.DataFram(d)
# d=pd.date_range("20010101","20200101").strftime('%Y%m%d')
# d=pd.Series(d)
#
# d.replace(',',' ,',inplace=True)
# d.to_json(r'e:\2020.json',orient='records')
#
# print(d)

# df = DataFrame(list(market.find({'date': {'$gte': '20190618'}, 'variety': 'EG'})))
# print(df)

# market.delete_many({'date': {'$gte': '20200208'}})
#
# begin = DataFrame(list(market.find({}).sort([('_id', -1)]).limit(1)))
# begin = begin['date'][0]
# print("lastdate: "+begin)