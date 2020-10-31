# encoding: utf-8
# %matplotlib inline
import pymongo, json
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt

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

def flows(futures, start=None, end=None, var=None,roll=None):
    position = futures.position
    market = futures.market
    # market1 = futures.p
    market = DataFrame(list(market.find({'date': {'$gte': start}, 'variety': var})))
    position = DataFrame(list(position.find({'date': {'$gte': start}, 'variety': var}))).drop_duplicates(['date','variety','symbol','long_party_name'], 'last')
    # position = position[['date','varie']]
    # position = position[position['long_party_name'].notna()]

    # 持仓
    # 所有会员
    party_name = position[position['date'] == end]
    long_party_name = party_name['long_party_name']
    short_party_name = party_name['short_party_name']
    party_name = long_party_name.append(short_party_name).dropna().drop_duplicates()
    # 多空变化量求和
    long = position.groupby(['date', 'variety', 'long_party_name'])[
        ['long_openIntr', 'long_openIntr_chg']].sum()
    # print(long)
    short = position.groupby(['date', 'variety', 'short_party_name'])[
        ['short_openIntr', 'short_openIntr_chg']].sum()
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
    # 价格变化量
    closes['change_index'] = closes.apply(lambda x: x['close_index'] - x['open_index'], axis=1)
    closes = closes.reset_index()

    chg = closes[['date', 'variety','close_index', 'change_index']]

    # print(chg['change_index'])

    # print(merge)
    df = pd.DataFrame()

    for i in party_name:
        try:
            chg = chg.copy()
            # print(chg)
            chg['BrokerID'] = i
            position1 = position[position['BrokerID']==i]
            # 两表合并
            mem = pd.merge(chg, position1, on=['date', 'variety','BrokerID'], how='left').fillna(0)
            # mem = merge[merge['BrokerID'] == i]
            # print(mem)


            mem = mem.copy()
            mem['today_net'] = mem.apply(lambda x: x['long_openIntr'] - x['short_openIntr'], axis=1)
            mem['yesterday_net'] = mem.groupby(['variety', 'BrokerID'])['today_net'].shift(1)
            mem['tomorrow_chg'] = mem.groupby(['variety', 'BrokerID'])['change_index'].shift(-1)
            mem['net_chg'] = mem.apply(lambda x: x['today_net'] - x['yesterday_net'], axis=1)
            #
            mem['count'] = mem['net_chg'].count()
            # mem = mem.rename(columns={'long_open_interest': 'long_openIntr', 'long_open_interest_chg': 'long_openIntr_chg', 'short_open_interest': 'short_openIntr','short_open_interest_chg': 'short_openIntr_chg'})
            # mem['change'] = mem.groupby(['variety', 'BrokerID'])['close_index'].shif(1)
            mem['change']=mem['close_index']-mem['close_index'].shift(1)




            # 时间窗口相关系数
            # mem['corr'] = mem['net_chg'].rolling(window=240).corr(mem['change_index'])
            # mem['corr2'] = mem['net_chg'].rolling(window=240).corr(mem['tomorrow_chg']).shift(1)
            # mem['corr3'] = mem['today_net'].rolling(window=240).corr(mem['change'])
            #
            mem['lot']=0
            # mem = mem.copy()
            mem['lot'] = mem.apply(lambda x: 0 if x['today_net'] == 0 else 1 if x['today_net'] > 0 else -1, axis=1)
            mem['lot'] = mem['lot'].shift(1).fillna(0)
            mem['pnl'] = mem['change'] * mem['lot']
            # mem['fee']=0
            # mem['fee'][mem['lot'] != mem['lot'].shif(1)] = mem['close_index'] * 2*1
            mem['netpnl'] = mem['pnl']
            mem['cumpnl'] = mem['netpnl'].rolling(roll).sum()

            # mem['date'] = pd.to_datetime(mem['date'])


            # #画图
            # mem = mem.set_index('date')
            # with pd.plotting.plot_params.use('x_compat', True):  # 方法一
            #     mem[['cumpnl']].plot(color='r',title=mem[u'BrokerID'][0]+" "+var+' '+end)
            #     mem['today_net'].plot(secondary_y=['today_net'])
            #     plt.ylabel('净持仓')
            # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
            # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
            # plt.show()



            # plt.plot(mem['cumpnl'])
            # print(mem)

            # flows = mem[mem['cumpnl'] > 0]
            # flows.sort_values('cumpnl', inplace=False)
            # print(flows)
            # # flows = flows[['date', 'variety', 'BrokerID', 'corr', 'corr2', 'today_net', 'net_chg', 'corr3',
            #                'cumpnl']].sort_values('cumpnl',
            #                                       inplace=False)  # [['date','variety','BrokerID','corr','corr2','cumpnl']]
            # flows = flows.rename(columns={'today_net': '净持仓', 'cumpnl': '累计盈亏点数', 'net_chg': '净持仓变化量', 'corr3': '相关系数'})
            # print(flows[['variety','BrokerID','净持仓','净持仓变化量','累计盈亏点数']])
            # print(flows)
            # print(flows.sort_values('累计盈亏点数'))
            # mem=mem.groupby()
            # print(mem)
            # print(flows['净持仓'].sum())

            # mem = mem[-1:]
            print(mem)

            df1 = pd.DataFrame(mem)
            df = df.append(df1)

            # print(df.tail(20))
        except:
            continue
    return df


if __name__ == '__main__':
    client = pymongo.MongoClient('localhost', 27017)
    futures = client.futures2

    start = '20190123'
    end = '20200324'
    var = 'JD'
    roll = 5
    f = flows(futures, start, end, var,roll)
    print(f)
    chg = f[['date','variety','close_index']].drop_duplicates()
    chg['change'] = chg['close_index'] - chg['close_index'].shift(1)
    # print(chg.tail(20))
    f = f[f['cumpnl']>0]
    mean = f.groupby(['date'])['cumpnl'].mean()[0]
    f = f[f['cumpnl'] > mean]

    # print(flows)

    # flows  = flows[['date','variety','BrokerID','close_index','today_net','net_chg','cumpnl']].sort_values('cumpnl',inplace=False)  #[['date','variety','BrokerID','corr','corr2','cumpnl']]
    # flows = flows.rename(columns={'today_net':'净持仓','cumpnl':'累计盈亏点数','net_chg':'净持仓变化量'})
    # print('0000000000')
    f =  f.groupby(['date','close_index','variety'])['today_net','BrokerID'].apply(lambda x:x.sum()).reset_index()
    # 两表合并
    # print(flows.tail(20))
    mem = pd.merge(chg, f, on=['date', 'variety','close_index'], how='left').fillna(0)
    # mem = mem.rename(columns={'change_index': 'change'})


    # flows = flows[['date','today_net','change','variety']]
    # mem = flows
    mem['lot'] = 0
    # mem = mem.copy()
    mem['lot'] = mem.apply(lambda x: 0 if x['today_net'] == 0 else 1 if x['today_net'] > 0 else -1, axis=1)
    mem['lot'] = mem['lot'].shift(1).fillna(0)
    mem['pnl'] = mem['change'] * mem['lot']
    # mem['fee']=0
    # mem['fee'][mem['lot'] != mem['lot'].shif(1)] = mem['close_index'] * 2*1
    mem['netpnl'] = mem['pnl']
    mem['cumpnl'] = mem['netpnl'].cumsum()
    print(mem.tail(20))

    # 画图
    mem = mem.set_index('date')
    with pd.plotting.plot_params.use('x_compat', True):  # 方法一
        mem[['cumpnl']].plot(color='r', title=start +'  '+ end  +' '+var)
        mem['today_net'].plot(secondary_y=['today_net'])
        plt.ylabel('净持仓')

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.show()