# encoding: utf-8

import pandas as pd
import tushare as ts
import datetime
import json
from pymongo import MongoClient

pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

if __name__ == '__main__':

    # 连接数据库
    client = MongoClient('localhost', 27017)
    db = client.futures
    marketdata = db.marketdata

    # 填写日期
    begin = datetime.date(2018, 9, 22)
    end = datetime.date(2018, 10, 21)
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        days = day.strftime('%Y-%m-%d')
        # 四大交易所行情
        dce = ts.get_dce_daily(days)
        shf = ts.get_shfe_daily(days)
        zce = ts.get_czce_daily(days)
        cff = ts.get_cffex_daily(days)
        frames = [dce, shf, zce, cff]
        try:
            # 合并四大交易所行情表
            df2 = pd.concat(frames)
            # df2 = df2.convert_objects(convert_numeric=True)
            df2 = df2.apply(pd.to_numeric, errors="ignore")
            df2 = df2.reset_index()
            print(df2)
            marketdata.insert(json.loads(df2.T.to_json()).values())

        #             print(json.loads(df2.T.to_json()).values())
        except:
            print(days, frames, '数据异常')
            continue