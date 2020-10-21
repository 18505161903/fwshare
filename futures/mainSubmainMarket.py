# encoding: utf-8

import pandas as pd
import datetime,time
import json
from pymongo import MongoClient
import fushare as f
from pandas import DataFrame
# from datetime import datetime

pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

# 连接数据库u
client = MongoClient('localhost', 27017)
db = client.futures34
mainSubmainMarket = db.mainSubmainMarket

# 填写日期

begin = datetime.date(2020, 3, 1)
# end = datetime.date(2010,8,24)
end = datetime.date.today()

for i in range((end - begin).days + 1):
    day = begin + datetime.timedelta(days=i)
    days = day.strftime('%Y%m%d')
    try:
        df=f.get_mainSubmain_bar(type = 'var', date = days)
        df = df.apply(pd.to_numeric, errors="ignore")
        print(df)

        # mainSubmainMarket.insert_many(df.to_dict('records'))
        # print(df.to_dict('records'))
    except:
        print(days, '数据异常')
    continue