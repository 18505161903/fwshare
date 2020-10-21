# encoding: utf-8
import pymongo
import pandas as pd
from pandas import DataFrame

# 更新conda自身 conda updae conda


pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

def flows2(futures,start=None,end=None,var=None):
    position = futures.position2
    market = futures.market2
    market = DataFrame(list(market.find({'date': {'$gte': start}, 'variety': var})))
    position = DataFrame(list(position.find({'date': {'$gte': start}, 'variety': var})))
    # mainSignal = futures.mainSignal
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
            mem['profit'] = mem.apply(lambda x: abs(x['tomorrow_chg']) if x['tomorrow_chg'] * x['net_chg']>0 else -abs(x['tomorrow_chg']), axis=1)
            mem['交易信号'] = mem.apply(lambda x: 0 if x['net_chg']==0  else 1 if x['net_chg']>0 else -1,axis=1)
            mem = mem.dropna()
            print(mem)
            # mem.to_csv(r"e:\fit.csv", mode='a', encoding='ANSI', header=True)




            # mem["net_profit"] = mem["profit"].cumsum()
            # plt.figure(figsize=(15, 21))
            # balance_plot = plt.subplot(4, 1, 1)
            # balance_plot.set_title("Balance")  # 资金曲线
            # mem["balance"].plot(legend=True)
            # mem.to_csv(r"e:\fit.csv", mode='a', encoding='ANSI', header=True)
            # print(mem)
            # mem=mem.dropna()

            # print(mem.head())
            if len(mem)<3:
                break
            mem['count'] = mem['net_chg'].count()
            #相关系数
            corr = mem['net_chg'].corr(mem['change_index'])
            corr2= mem['net_chg'].corr(mem['tomorrow_chg'])
            ends = mem[mem['date'] == end]
            ends=ends.copy()
            ends['corr'] = corr
            ends['corr2'] = corr2
            ends['start'] = start
            ends['net_profit'] =  mem["net_profit"].shift(1)
            df1 = pd.DataFrame(ends)
            df = df.append(df1)

        except:
            continue
    return df

if __name__ == '__main__':

    client = pymongo.MongoClient('localhost', 27017)
    futures = client.futures2

    start = '20190101'
    end = '20200210'
    var = 'JD'
    flows=flows2(futures,start,end,var)
    print(flows)#.sort_values('corr',ascending=True)