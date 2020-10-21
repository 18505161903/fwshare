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
    marketdata = db.marketdata

    # 填写日期
    begin = datetime.date(2016,1, 1)
    end = datetime.date(2019, 5, 30)
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        days = day.strftime('%Y%m%d')
        # 四大交易所行情
        dce = fushare.get_dce_daily(days)
        shf = fushare.get_shfe_daily(days)
        zce = fushare.get_czce_daily(days)
        cff = fushare.get_cffex_daily(days)
        frames = [shf,zce,dce,cff]

        try:
            # 合并四大交易所行情表
            df2 = pd.concat(frames)
            # 计算品种价格变化量
            df2 = df2.dropna(axis=0, how='any')
            df2 = df2.apply(pd.to_numeric, errors="ignore")
            df2['change'] = df2['close'] - df2['open']
            df2['date'] = days
            df2 = df2.dropna(axis=0, how='any')
            df2 = df2.reset_index()
            print(df2.head())
            df2 = df2[['date', 'variety','symbol', 'close','open','high','low','volume','open_interest','turnover','settle','pre_settle','change']]
            # print(df2)
            marketdata.insert(json.loads(df2.T.to_json()).values())
            print(json.loads(df2.T.to_json()).values())
        except:
            print(days, '数据异常')
            continue