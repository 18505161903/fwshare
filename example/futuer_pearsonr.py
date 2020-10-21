# encoding: utf-8
import pymongo,json
import pandas as pd
from pandas import Series,DataFrame
from scipy.stats import pearsonr


pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行
def wh(var='NI',start='20190105',end='20190627'):
    client = pymongo.MongoClient('localhost', 27017)
    futures = client.futures
    position = futures.position
    market = futures.indexMarket

    market = DataFrame(list(market.find({'date': {'$gte': start}})))
    position = DataFrame(list(position.find({'date': {'$gte': start}})))

    # 整理期货公司
    party_name = position[position['date'] >= end]
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
        print(mem)
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
        chgs = hb['change']
        nets = hb['净持仓变化量']

        todayNetpostion = all_position[all_position['date']==end]
        # #相关系数
        p = pearsonr(chgs, nets)[0]
        # r = pearsonr(chgs, nets)[1]
        try:
            # print(var,start,end,i,p,all_position['净持仓变化量'].count(),todayNetpostion['当日净持仓'].values[0],all_position['净持仓变化量'].values[0])
            print(var,start,end,i)
        except:
            continue
if __name__ == '__main__':
    wh(var='NI',start='20190101',end='20200105')
    # print(wh)
