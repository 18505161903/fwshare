# encoding: utf-8

import pandas as pd
import datetime
import json
from pymongo import MongoClient
import fushare
print(fushare.__version__)
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

if __name__ == '__main__':

    # 连接数据库
    client = MongoClient('localhost', 27017)
    db = client.futures
    indexMarket = db.indexMarket

    # 填写日期
    begin = datetime.date(2019, 10, 25)
    end = datetime.date(2019, 10,25)
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        days = day.strftime('%Y%m%d')
        # 四大交易所行情
        dce = fushare.get_dce_daily(days)
        shf = fushare.get_shfe_daily(days)
        zce = fushare.get_czce_daily(days)
        cff = fushare.get_cffex_daily(days)
        frames = [dce,shf,zce,cff]

        try:
            # 合并四大交易所行情
            df2 = pd.concat(frames)
            # 计算品种指数收盘价
            df2 = df2.dropna(axis=0, how='any')
            # df2 = df2.convert_objects(convert_numeric=True)
            df2 = df2.apply(pd.to_numeric, errors="ignore")
            df2['closev'] = df2['close'] * df2['volume']
            df2['openv'] = df2['open'] * df2['volume']
            df2['highv'] = df2['high'] * df2['volume']
            df2['lowv'] = df2['low'] * df2['volume']
            df2 = df2.groupby('variety')['volume', 'closev','openv','highv','lowv'].sum()
            df2['set_close'] = round(df2['closev'] / df2['volume'])
            df2['set_open'] = round(df2['openv'] / df2['volume'])
            df2['set_high'] = round(df2['highv'] / df2['volume'])
            df2['set_low'] = round(df2['lowv'] / df2['volume'])
            df2['change'] = df2['set_close'] - df2['set_open']
            df2['date'] = days
            df2 = df2.dropna(axis=0, how='any')
            df2 = df2.reset_index()
            df2 = df2[['date', 'variety', 'set_close','set_open','set_high','set_low','change']]
            # print(df2)
            indexMarket.insert_many(json.loads(df2.T.to_json()).values())
            print(json.loads(df2.T.to_json()).values())
        except:
            print(days, '数据异常')
            continue