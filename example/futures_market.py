# encoding: utf-8

import pandas as pd
import datetime
import json
from pymongo import MongoClient
import fushare
import time
print(fushare.__version__)
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

if __name__ == '__main__':

    # 连接数据库
    client = MongoClient('localhost', 27017)
    db = client.futures5
    market = db.market

    # 填写日期
    begin = datetime.date(2019,9,12)
    end = datetime.date(2019,9, 12)
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        days = day.strftime('%Y%m%d')
        # 四大交易所行情
        # shf = fushare.get_shfe_daily(days)
        zce = fushare.get_czce_daily(days)
        cff = fushare.get_cffex_daily(days)
        dce = fushare.get_dce_daily(days)
        frames = [cff,dce]
        # time.sleep(1)
        try:
            # 合并四大交易所行情
            df2 = pd.concat(frames)
            # 数字化，添加日期列
            df2 = df2.dropna(axis=0, how='any')
            df2 = 1
            df2['date'] = days
            df2 = df2.dropna(axis=0, how='any')
            df2 = df2.reset_index()
            market.insert_many(json.loads(df2.T.to_json()).values())

            print(json.loads(df2.T.to_json()).values())
        except:
            print(days, '数据异常')
            continue