# encoding: utf-8
import pymongo,json
import pandas as pd
from pandas import Series,DataFrame
from scipy.stats import pearsonr

import copy
from datetime import datetime, date, timedelta

pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

def wh(var='NI'):
    client = pymongo.MongoClient('localhost', 27017)
    futures = client.futures
    unit = futures.unit
    position = futures.position
    market = futures.market
    positions = futures.positions

    market = DataFrame(list(market.find({'date': {'$gte': '20181101'}})))
    position = DataFrame(list(position.find({'date': {'$gte': '20181101'}})))

    # 整理期货公司
    party_name = position[position['date'] >= '20181123']

    party_name = party_name[party_name['variety'] == var]
    long_party_name = party_name['long_party_name']
    short_party_name = party_name['short_party_name']
    party_name = long_party_name.append(short_party_name)
    party_name = party_name.drop_duplicates(keep='first').dropna()
    long = position.groupby(['date', 'variety', 'long_party_name'])[['long_openIntr']].sum()
    short = position.groupby(['date', 'variety', 'short_party_name'])[['short_openIntr']].sum()
    # 合并
    frames = [long, short]
    position = pd.concat(frames, axis=1, sort=True).fillna(0).reset_index()
    # 净持仓
    position['净持仓'] = position.apply(lambda x: x['long_openIntr'] - x['short_openIntr'], axis=1)
    # 字段更名
    position = position.rename(columns={'level_0': 'date', 'level_1': 'variety', 'level_2': 'mem'})
    vars = position[position['variety'] == var]
    for i in party_name:
        mem = vars[vars['mem'] == i]
        # print(mem)
        position_behind = mem.shift(1)
        # # 合并滞后和原始数据
        all_position = pd.merge(position, position_behind, right_index=True, left_index=True)
        # print(all_position)
        all_position = all_position[
            ['date_x', 'variety_x', 'mem_x', 'long_openIntr_x', 'short_openIntr_x', '净持仓_x', '净持仓_y']].dropna()
        # print(all_position)
        all_position['净持仓变化量'] = all_position.apply(lambda x: x['净持仓_x'] - x['净持仓_y'], axis=1)
        # print(all_position)
        # 更名
        all_position = all_position.rename(
            columns={'date_x': 'date', 'variety_x': 'variety', 'mem_x': 'mam', 'long_openIntr_x': 'long_openIntr',
                     'short_openIntr_x': 'short_openIntr', '净持仓_x': '当日净持仓', '净持仓_y': '昨日净持仓'})
        # # #涨跌数
        market['change'] = market.apply(lambda x: x['set_close'] - x['set_open'], axis=1)
        vars1 = market[market['variety'] == var]
        chg = vars1[['date', 'variety', 'change']]
        # # 合并
        hb = pd.merge(chg, all_position, on=['date', 'variety'], how='outer').dropna().drop_duplicates()

        # df=pd.DataFrame(hb)
        chgs = hb['change']
        nets = hb['净持仓变化量']
        # #相关系数
        p = pearsonr(chgs, nets)
        print(i, p)

    # print(df.tail(1))
    #     chgs=df['change']
    #     nets=df['净持仓变化量']
    #     try:
    #         p=pearsonr(chgs,nets)[0]
    #         print(i,p)
    #     except:
    #         continue
if __name__ == '__main__':
    wh(var='MA')