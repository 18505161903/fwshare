# encoding: utf-8

import pandas as pd
import datetime,time
import json
from pymongo import MongoClient
import fushare as ak
# import fushare as ak
from pandas import DataFrame
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

if __name__ == '__main__':

    # 连接数据库
    client = MongoClient('localhost', 27017)
    db = client.futures2
    market = db.position

    # 填写日期
    today = datetime.date.today()
    end=today
    begin = DataFrame(list(market.find({}).sort([('_id', -1)]).limit(1)))
    begin = begin['date'][0]
    begin = time.strptime(begin, "%Y%m%d")
    year, month, day = begin[:3]
    begin = datetime.date(year, month, day)
    begin = begin + datetime.timedelta(days=1)
    print(begin)


import ft2