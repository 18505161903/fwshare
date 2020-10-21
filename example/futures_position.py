# encoding: utf-8
import datetime
import pandas as pd

import json
from pymongo import MongoClient
import fushare
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

def get_trade_rank(market = 'SHF', date = None):
    if date is None:
        date = get_target_date(-1, "%Y-%m-%d")
    if market == 'SHF':
        return fushare.get_shfe_rank_table(date)
    if market == 'DCE':
        return fushare.get_dce_rank_table(date)
    if market == 'CZC':
        return fushare.get_czce_rank_table(date)
    if market == "CFE":
        return fushare.get_cffex_rank_table(date)
    return None, '不支持的市场类型'

if __name__ == '__main__':

    markets = ['SHF']#, 'CZC', 'SHF','CFE','DCE'
    # 连接数据'C'CZC', 'SHF','CFE','DCE'ZC', 'SHF','CFE','DCE'库
    client = MongoClient('localhost', 27017)
    db = client.futures5
    position = db.position
    for market in markets:
        begin = datetime.date(2019,6,19)
        end = datetime.date(2019, 1, 8)

        for i in range((end - begin).days + 1):
            day = begin + datetime.timedelta(days=i)
            days=day.strftime('%Y%m%d')
            try:
                df = get_trade_rank(market, date=days)
                print(days, market)
                for key, value in df.items():
                    value['date'] = days

                    if market != 'CZC':
                        print('insert into',key)
                        position.insert(json.loads(value.T.to_json()).values())
                    else:
                        value=value[value['symbol']==value['variety']]
                        print('insert into',key)
                        position.insert(json.loads(value.T.to_json()).values())
            except:
                print(days,market,'数据异常')
                continue
