# encoding: utf-8
import pymongo,json
import pandas as pd
from pandas import DataFrame
#
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行


# client = pymongo.MongoClient('localhost', 27017)
# futures = client.futures_ak
#
# start = '20190101'
# end ='20200207'
# var = 'MA'

def flows(futures,start=None,end=None,var=None):

    position = futures.position
    market = futures.market
    # market1 = futures.p
    market = DataFrame(list(market.find({'date': {'$gte': start}, 'variety': var})))
    position = DataFrame(list(position.find({'date': {'$gte': start}, 'variety': var})))
    # position = position[position['long_party_name'].notna()]

    #持仓
    #所有会员
    party_name = position[position['date'] == end]
    long_party_name = party_name['long_party_name']
    short_party_name = party_name['short_party_name']
    party_name = long_party_name.append(short_party_name).dropna().drop_duplicates()
    #多空变化量求和
    long = position.groupby(['date', 'variety', 'long_party_name'])[['long_open_interest', 'long_open_interest_chg']].sum()
    # print(long)
    short = position.groupby(['date', 'variety', 'short_party_name'])[['short_open_interest', 'short_open_interest_chg']].sum()
    # # 合并
    frames = [long, short]
    position = pd.concat(frames, axis=1, sort=True).fillna(0).reset_index()
    # 字段更名
    position = position.rename(columns={'level_0': 'date', 'level_1': 'variety', 'level_2': 'BrokerID'})
    #
    ##行情
    market = market.copy()
    # 指数收盘
    market['cv'] = market.apply(lambda x: x['close'] * x['open_interest'], axis=1)
    closes = market.groupby(['date', 'variety'])[['cv', 'open_interest']].sum()
    closes['close_index'] = closes['cv'] / closes['open_interest']
    # #指数开盘
    market['ov'] = market.apply(lambda x: x['open'] * x['open_interest'], axis=1)
    opens = market.groupby(['date', 'variety'])[['ov', 'open_interest']].sum()
    closes['open_index'] = opens['ov'] / opens['open_interest']
    #价格变化量
    closes['change_index'] = closes.apply(lambda x: x['close_index'] - x['open_index'], axis=1)
    closes = closes.reset_index()


    chg = closes[['date', 'variety', 'change_index']]
    # print(chg['change_index'])

    #两表合并
    # merge = pd.merge(position, chg, on=['date', 'variety'], how='outer').dropna().drop_duplicates()

    df = pd.DataFrame()
    for i in party_name:
        try:
            chg = chg.copy()
            chg['BrokerID'] = i
            position1 = position[position['BrokerID'] == i]
            # 两表合并
            mem = pd.merge(chg, position1, on=['date', 'variety', 'BrokerID'], how='left').fillna(0)
            # mem = merge[merge['BrokerID'] == i]

            mem = mem.copy()
            mem['today_net'] = mem.apply(lambda x: x['long_open_interest'] - x['short_open_interest'], axis=1)

            mem['yesterday_net']= mem.groupby(['variety', 'BrokerID'])['today_net'].shift(1)
            mem['tomorrow_chg'] = mem.groupby(['variety', 'BrokerID'])['change_index'].shift(-1)
            mem['net_chg'] = mem.apply(lambda x: x['today_net'] - x['yesterday_net'], axis=1)
            mem['count'] = mem['net_chg'].count()

            # print(mem)
            #时间窗口相关系数
            mem['corr'] = mem['net_chg'].rolling(window=240).corr(mem['change_index'])
            mem['corr2'] = mem['net_chg'].rolling(window=240).corr(mem['tomorrow_chg'])
            print(mem)
            mem=mem[-1:]
            # mem['start'] = mem['date'].values[0]
            # print(mem)
            #
            # market1.insert(json.loads(mem.T.to_json()).values())
            # print(json.loads(mem.T.to_json()).values())
            # ends = mem[mem['date'] == end]
            # ends=ends.copy()

            df1 = pd.DataFrame(mem)
            df = df.append(df1)
            # print(df)
        except:
            continue
    return df

if __name__ == '__main__':

    client = pymongo.MongoClient('localhost', 27017)
    futures = client.futures3

    start = '20190101'
    end ='20200311'
    var = 'M'
    flows=flows(futures,start,end,var)
    print(flows)
    # print(flows)