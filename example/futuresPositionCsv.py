# encoding: utf-8

from opendatatools import futures
import datetime, os
import pandas as pd
import time

if __name__ == '__main__':
    begin_year = 2018
    end_year = 2018
    begin_month = 7
    end_month = 7
    begin_day = 5
    end_day = 10
    time_sleep = 3
    # markets = ['SHF']
    markets = ['SHF', 'CZC', 'DCE', 'CFE']  # , 'SHF','CZC', 'DCE', 'CFE'
    if os.path.exists(r"c:\FuturesPosition.csv"):
        os.remove(r"c:\FuturesPosition.csv")
    for market in markets:
        begin = datetime.date(begin_year, begin_month, begin_day)
        end = datetime.date(end_year, end_month, end_day)
        for i in range((end - begin).days + 1):
            day = begin + datetime.timedelta(days=i)
            days = day.strftime('%Y-%m-%d')
            print(days)
            # df, msg = futures.get_trade_rank(market, date=days)
            try:
                # df, msg = futures.get_trade_rank(market, date='2014-06-05')
                df, msg = futures.get_trade_rank(market, date=days)
            except:
                print(days, market, '数据异常')
                continue
            if os.path.exists(r"C:/FuturesPosition.csv"):
                df.to_csv(r"C:/FuturesPosition.csv", mode='a', encoding='ANSI', header=False)
            else:
                df.to_csv(r"C:/FuturesPosition.csv", encoding='ANSI')

    time.sleep(time_sleep)
    df = pd.read_csv('C:/FuturesPosition.csv', encoding='ANSI')
    df = df[['date', 'variety', '持买仓量', '持卖仓量']]
    a = []
    b = []
    aa = []
    bb = []
    cc = []
    for i in df['持买仓量']:
        i = str(i)
        i = i.replace(',', '')
        i = i.replace('-', '')
        if i == '':
            a.append(0)
        else:
            i = float(i)
            a.append(i)
    for i in df['持卖仓量']:
        i = str(i)
        i = i.replace(',', '')
        i = i.replace('-', '')
        if i == '':
            b.append(0)
        else:
            i = float(i)
            b.append(i)
    df['持买仓量'] = a
    df['持卖仓量'] = b
    df = df.groupby(['date', 'variety']).sum()
    df['净持仓'] = df['持买仓量'] - df['持卖仓量']

    df.to_csv('C:/FuturesPosition.csv', encoding='ANSI')

    time.sleep(time_sleep)
    a = []
    b = []
    c = []
    df = pd.read_csv('C:/FuturesPosition.csv', encoding='ANSI')
    if len(str(begin_month)) == 1:
        begin_month = '0' + str(begin_month)
    if len(str(end_month)) == 1:
        end_month = '0' + str(end_month)
    if len(str(begin_day)) == 1:
        begin_day = '0' + str(begin_day)
    if len(str(end_day)) == 1:
        end_day = '0' + str(end_day)
    df1 = df[df['date'] == str(begin_year) + '/' + str(begin_month) + '/' + str(begin_day)]['净持仓']
    df2 = df[df['date'] == str(end_year) + '/' + str(end_month) + '/' + str(end_day)]['净持仓']
    for i in df1:
        a.append(i)
    for i in df2:
        b.append(i)
    for i in range(len(a)):
        c.append(b[i] - a[i])
    df = df[df['date'] == str(end_year) + '/' + str(end_month) + '/' + str(end_day)]
    df['净持仓变化量'] = c
    df.to_csv('C:/FuturesPosition.csv', encoding='ANSI', index=False)