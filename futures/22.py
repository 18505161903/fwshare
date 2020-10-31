# encoding: utf-8
# import tensorflow as tf
import datetime
import pandas as pd
import json
from pymongo import MongoClient
import fushare as ak

pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

def get_trade_rank(market = 'SHF', date = None):
    if date is None:
        date = get_target_date(-1, "%Y-%m-%d")
    if market == 'SHF':
        return ak.get_shfe_rank_table(date)
    if market == 'DCE':
        return ak.get_dce_rank_table(date)
    if market == 'CZC':
        return ak.get_czce_rank_table(date)
    if market == "CFE":
        return ak.get_cffex_rank_table(date)
    return None, '不支持的市场类型'

if __name__ == '__main__':

    markets = ['CZC', 'SHF','CFE','DCE']#, 'CZC', 'SHF','CFE','DCE'
    # 连接数据库
    client = MongoClient('localhost', 27017)
    db = client.futures2
    position = db.position

    df=pd.DataFrame()
    for market in markets:
        begin = datetime.date(2020,7,22)
        end = datetime.date(2020,10,12)
        # end = datetime.date.today()

        for i in range((end - begin).days + 1):
            day = begin + datetime.timedelta(days=i)
            days=day.strftime('%Y%m%d')
            try:
                df = get_trade_rank(market, date=days)
                # print(days, market)
                for key, value in df.items():
                    value['date'] = days
                    value['symbol'] = value['symbol'].str.upper()

                    # vars = position[position['variety'] == var]
                    # position.insert(json.loads(value.T.to_json()).values())
                    # print(value)

                    #去除具体合约。因汇总持仓有问题
                    if market != 'CZC':
                        # print('insert into',key)
                        position.insert_many(json.loads(value.T.to_json()).values())
                    else:
                        value=value[value['symbol']==value['variety']]
                        # print('insert into',key)
                        # print(value)
                        # position.insert_many(json.loads(value.T.to_json()).values())
                        # print(json.loads(value.T.to_json()).values())
                        df=df.append(value)
                        print()
            except:
                print(days,market,'数据异常')
                continue


 #所有会员
party_name = value[value['date'] == end]
long_party_name = party_name['long_party_name']
short_party_name = party_name['short_party_name']
party_name = long_party_name.append(short_party_name).drop_duplicates()
#多空变化量求和
long = value.groupby(['date', 'variety', 'long_party_name'])['long_openIntr'].sum()
# print(long)
short = value.groupby(['date', 'variety', 'short_party_name'])['short_openIntr'].sum()
# # 合并
frames = [long, short]
position = pd.concat(frames, axis=1, sort=True).fillna(0).reset_index()
position


 # 字段更名
position = position.rename(columns={'level_0': 'date', 'level_1': 'variety', 'level_2': 'BrokerID'})

然后保存excel

