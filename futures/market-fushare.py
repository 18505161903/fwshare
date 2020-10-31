# encoding: utf-8

import pandas as pd
import datetime,time
import json
from fushare.dailyBar import get_future_daily
# from pymongo import MongoClient
import fushare as ak
# import fushare as ak
from pandas import DataFrame
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

if __name__ == '__main__':

    # 连接数据库
    # client = MongoClient('localhost', 27017)
    # db = client.futures2
    # market = db.market3

    # 填写日期
    begin = datetime.date(2020,10,20)
    end = datetime.date(2020,10,20)

    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        days = day.strftime('%Y%m%d')

        df = pd.DataFrame()
        for market in ['dce', 'cffex', 'shfe', 'czce']:
            try:
                df = df.append(get_future_daily(start=begin, end=end, market=market))
                print(df)
            #写入db
            # market.insert_many(json.loads(df2.T.to_json()).values())
            # print(json.loads(df2.T.to_json()).values())
            except:
                print(days, '数据异常')
                continue

