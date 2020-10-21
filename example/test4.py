# encoding: utf-8

import pandas as pd
import datetime
import json
from pymongo import MongoClient
import tushare as fushare
print(fushare.__version__)
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

if __name__ == '__main__':

    # 连接数据库
    client = MongoClient('localhost', 27017)
    db = client.futures
    market = db.market

    # 填写日期
    begin = datetime.date(2019,6, 10)
    end = datetime.date(2019,6, 10)

    pro = fushare.pro_api('c0cad8f56caba4e70702d606290d04f88514a6bef046f60d13144151')




    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        days = day.strftime('%Y%m%d')
        # df = pro.fut_daily(trade_date=days, exchange='',
        #                    fields='ts_code,trade_date,pre_close,pre_settle,open,high,low,close,settle,vol')

        df = pro.fut_holding(trade_date=days)
        frames = [df]
        print(df)


        try:
            # 合并四大交易所行情
            df2 = pd.concat(frames)
            # 计算品种指数收盘价
            df2 = df2.dropna(axis=0, how='any')
            # df2 = df2.convert_objects(convert_numeric=True)
            df2 = df2.apply(pd.to_numeric, errors="ignore")
            df2['closev'] = df2['close'] * df2['volume']
            df2['openv'] = df2['open'] * df2['volume']
            df2 = df2.groupby('variety')['volume', 'closev','openv'].sum()
            df2['set_close'] = round(df2['closev'] / df2['volume'])
            df2['set_open'] = round(df2['openv'] / df2['volume'])
            df2['change'] = df2['set_close'] - df2['set_open']
            df2['date'] = days
            df2 = df2.dropna(axis=0, how='any')
            df2 = df2.reset_index()
            df2 = df2[['date', 'variety', 'set_close','set_open','change']]
            # print(df2)
            market.insert(json.loads(df2.T.to_json()).values())
            print(json.loads(df2.T.to_json()).values())
        except:
            print(days, '数据异常')
            continue