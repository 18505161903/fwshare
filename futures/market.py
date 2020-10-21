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
    market = db.market3

    # 填写日期
    # today = datetime.date.today()
    # end=today
    # begin = DataFrame(list(market.find({}).sort([('_id', -1)]).limit(1)))
    # begin = begin['date'][0]
    # begin = time.strptime(begin, "%Y%m%d")
    # year, month, day = begin[:3]
    # begin = datetime.date(year, month, day)
    # begin = begin + datetime.timedelta(days=1)

    begin = datetime.date(2013, 4, 9)
    end = datetime.date(2020, 8, 11)

    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        days = day.strftime('%Y%m%d')
        # 四大交易所行情
        dce =ak.get_dce_daily(days)
        # shf =ak.get_shfe_daily(days)
        # zce =ak.get_czce_daily(days)
        # cff = ak.get_cffex_daily(days)
        frames = [dce]#dce,shf,zce,cff

        try:
            # 合并四大交易所行情表
            df2 = pd.concat(frames)
            df2 = df2.dropna(axis=0, how='any')
            df2 = df2.apply(pd.to_numeric, errors="ignore")
            df2 = df2.reset_index()
            df2['date'] = days
            # print(df2.info())
            del df2['index']
            market.insert_many(json.loads(df2.T.to_json()).values())
            print(json.loads(df2.T.to_json()).values())
        except:
            print(days, '数据异常')
            continue

