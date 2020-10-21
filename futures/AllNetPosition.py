# encoding: utf-8
# import tensorflow as tf

import datetime
from time import time
import pandas as pd
import akshare as ak

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
def handle(path):
    """
    handle data
    - 去除逗号，
    - 转化为浮点数类型
    """
    markets = ['CZC', 'SHF', 'DCE']
    df = pd.DataFrame()
    for market in markets:
        # begin = datetime.date(2020, 10, 20)
        # end = datetime.date(2020, 10, 20)
        begin = datetime.date.today()
        end = begin
        print(str(begin)+' 正在拉取'+market+'...')
        for i in range((end - begin).days + 1):
            day = begin + datetime.timedelta(days=i)
            days = day.strftime('%Y%m%d')
            try:
                df1 = get_trade_rank(market, date=days)
                for key, value in df1.items():
                    value['date'] = days
                    if market == 'CZC':
                        value = value[value['symbol'] == value['variety']]
                        value = value.applymap(lambda x: x.replace(',', '').replace("-", ""))
                        df = df.append(value)
                        print('拉取了' + market+' '+df['symbol'].iloc[-1])
                    if market == 'SHF':
                        value = value[-value['rank'].isin([999])]
                        df = df.append(value)
                        print('拉取了' + market + ' ' + df['symbol'].iloc[-1])
                    if market == 'DCE':
                        value = value[-value['rank'].isin([999])]
                        # value = value.applymap(lambda x: x.replace(',', '').replace("-", ""))
                        df = df.append(value)
                        print('拉取了' + market+' '+df['symbol'].iloc[-1])
                    if market == 'CFE':
                        value = value[-value['rank'].isin([999])]
                        df = df.append(value)
                        print('拉取了' + market+' '+df['symbol'].iloc[-1])
            except:
                print(days, market, '数据异常')
                continue
    df = df.apply(pd.to_numeric, errors="ignore")
    #净持仓
    long = df.groupby(['date', 'variety', 'long_party_name'])[
        ['long_open_interest']].sum()
    short = df.groupby(['date', 'variety', 'short_party_name'])[
        ['short_open_interest']].sum()
    # # 合并
    frames = [long, short]
    position = pd.concat(frames, axis=1, sort=True).fillna(0).reset_index()
    # 字段更名
    position = position.rename(columns={'level_0': 'date', 'level_1': 'variety', 'level_2': 'BrokerID'})
    position['net'] = position.apply(lambda x: x['long_open_interest'] - x['short_open_interest'], axis=1)
    party_names = ['永安期货', '海通期货', '中信期货']
    df = pd.DataFrame()
    for i in party_names:
        try:
            mem = position[position['BrokerID'] == i]
            df1 = pd.DataFrame(mem)
            df = df.append(df1)
        except:
            print('?')
            continue
    two_level_index_series = df.set_index(['date','variety', 'BrokerID'])['net']
    net_df = two_level_index_series.unstack()
    net_df['合计'] = net_df.apply(lambda x: x.sum(), axis=1)
    net_df = net_df.rename_axis(columns=None).reset_index()
    net_df = net_df[['date','variety', '永安期货', '海通期货', '中信期货', '合计']]
    # print(net_df)
    net_df.to_excel(path, index=False)
    print(net_df)
    print('写入文件成功，保存路径： '+path)
    return net_df

if __name__ == '__main__':
    start = time()
    print("Start: " + str(start))
    filePath='D:/PyFile/AllNetPosition.xlsx'
    handle(filePath)
    for i in range(1, 100000000):
        pass
    stop = time()
    print("Stop: " + str(stop))
    print('Time spent：'+str(stop - start) + "秒")