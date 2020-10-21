# -*- coding:utf-8 -*-
import numpy as np
from fushare.symbolVar import *
from fushare.dailyBar import *
from fushare.cot import *
from fushare.cons import *
import tushare as ts
import math
import matplotlib as plot

pro = ts.pro_api('c0cad8f56caba4e70702d606290d04f88514a6bef046f60d13144151')

calendar = cons.get_calendar()

pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

def get_mainSubmainMarket_bar(type = 'symbol',  var = 'RB',date= None, start = None, end = None):

    date = cons.convert_date(date) if date is not None else datetime.date.today()
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    start = cons.convert_date(start) if start is not None else datetime.date.today()
    end = cons.convert_date(end) if end is not None else cons.convert_date(cons.get_latestDataDate(datetime.datetime.now()))

    if type == 'symbol':
        df = get_future_daily(start=date, end=date, market=symbolMarket(var))
        df = df[df['variety'] == var]
        # print(df)
        return df

    if type == 'var':
        df = pd.DataFrame()
        for market in ['dce','shfe','czce']:
            df = df.append(get_future_daily(start=date, end=date, market=market))
        varList = list(set(df['variety']))
        # print(varList)

        dfL=pd.DataFrame()
        for var in varList:
            try:
                ry = get_mainSubmainMarket(date, var, df = df)
                if ry:

                    dfL = dfL.append(pd.DataFrame([ry], index=[var], columns=['差价','basicPrice','symbol1','symbol2','M-differ']))
            except:
                pass
        dfL['date'] = date
        dfL = dfL.sort_values('basicPrice')
        dfL = dfL[(dfL['basicPrice'] >= 2) | (dfL['basicPrice'] <= -2)]
        dfL=dfL[dfL['M-differ']<=0]
        return dfL


def get_mainSubmainMarket(date = None, var = 'IF',symbol1 = None, symbol2 = None,c=None,df = None):

    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    if symbol1:
        var = symbol2varietie(symbol1)
        # print(var)
    if type(df) != type(pd.DataFrame()):
        market = symbolMarket(var)
        df = get_future_daily(start=date, end=date, market=market)
    if var:
        df = df[df['variety'] == var].sort_values('open_interest', ascending=False)
        df['close'] = df['close'].astype('float')
        # print(df)
        symbol1 = df['symbol'].tolist()[0]
        symbol2 = df['symbol'].tolist()[1]

    close1 = df['close'][df['symbol'] == symbol1.upper()].tolist()[0]
    close2 = df['close'][df['symbol'] == symbol2.upper()].tolist()[0]

    A = re.sub(r'\D', '', symbol1)
    A1 = int(A[:-2])
    A2 = int(A[-2:])
    B = re.sub(r'\D', '', symbol2)
    B1 = int(B[:-2])
    B2 = int(B[-2:])
    c = (A1 - B1) * 12 + (A2 - B2)

    if close1 == 0 or close2 == 0:
        return False
    if c > 0:
        return close1-close2,round((close1-close2)/close1/c*100,2), symbol1,symbol2,c
    else:
        return close2-close1,round((close2-close1)/close2/c*100,2), symbol1,symbol2,c


def get_mainSubmainPosition(date = None, var = 'IF',symbol1 = None, symbol2 = None,c=None,df = None):

    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    if symbol1:
        var = symbol2varietie(symbol1)
        # print(var)
    if type(df) != type(pd.DataFrame()):
        market = symbolMarket(var)
        df = get_future_daily(start=date, end=date, market=market)
        varList = list(set(df['variety']))

    if var:
        df = df[df['variety'] == var].sort_values('open_interest',ascending=False)
        # print(df)
        df['close'] = df['close'].astype('float')
        # # print(df)
        symbol1 = df['symbol'].tolist()[0]
        symbol2 = df['symbol'].tolist()[1]

        fut1= pro.fut_holding(trade_date=date.strftime('%Y%m%d'),symbol=symbol1).dropna(axis=0, how='any')
        fut2 = pro.fut_holding(trade_date=date.strftime('%Y%m%d'), symbol=symbol2).dropna(axis=0, how='any')

        fut1['netPosition1'] = fut1.apply(lambda x: x['long_hld'] - x['short_hld'], axis=1)
        fut2['netPosition2'] = fut2.apply(lambda x: x['long_hld'] - x['short_hld'], axis=1)


        df2=pd.merge(fut1,fut2,on=['trade_date','broker'],how='outer').dropna()
        df2=df2[['trade_date','broker','symbol_x','netPosition1','symbol_y','netPosition2']]
        df2=df2.rename(columns={'trade_date':'date','symbol_x':'symbol1','symbol_y':'symbol2'})

        df3=df2.loc[(df2['netPosition1']>0) & (df2['netPosition2']<0)]
        df4 = df2.loc[(df2['netPosition1']<0) & (df2['netPosition2']>0)]
        df2=pd.concat([df3,df4])

        def valabs1(row):
            row['absvalue1'] = row['netPosition1'].abs()
            return row
        valabs11= df2.groupby(['date','symbol1']).apply(valabs1)

        def valabs2(row):
            row['absvalue2'] = row['netPosition2'].abs()
            return row
        valabs22= df2.groupby(['date', 'symbol2']).apply(valabs2)
        df2=pd.merge(valabs11,valabs22,how='left')

        # df= df2.groupby(['date','broker','symbol1']).apply(lambda x:x['netPosition1'].abs()).reset_index()

        df2['ArbitrageFund']= df2.apply(lambda x: x['absvalue1']if x['absvalue1']<x['absvalue2']  else x['absvalue2'] if x['absvalue1']>x['absvalue2']else 0 ,axis=1)
        df2=df2.sort_values(['ArbitrageFund'])
        df=df2[['date','broker','symbol1','netPosition1','symbol2','netPosition2','ArbitrageFund']]
        df=df[df['broker']!='期货公司会员']

    return df
        # print(data)

if __name__ == '__main__':

    date = '20200929'

    df=pd.DataFrame()
    for i in cons.vars:
        try:
            d = get_mainSubmainPosition(date,i)
            df=df.append(d)
            # print(df)
        except:
            pass
    valsort=df.sort_values('ArbitrageFund',ascending=False)
    print(valsort)


    # data =get_mainSubmainMarket_bar(date=date, type='var')
    # print(data)
