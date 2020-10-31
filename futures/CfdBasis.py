# -*- coding:utf-8 -*-
from fushare.dailyBar import *
from fushare.cot import *
from fushare.cons import *
import pandas as pd
from pymongo import MongoClient

calendar = cons.get_calendar()
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

def get_mainSubmainMarket_bar(type = 'symbol',  var = 'RB',date= None, start = None, end = None):

    date = cons.convert_date(date) if date is not None else datetime.date.today()
    # start = cons.convert_date(start) if start is not None else datetime.date.today()
    # end = cons.convert_date(end) if end is not None else cons.convert_date(cons.get_latestDataDate(datetime.datetime.now()))

    if type == 'symbol':
        df = get_future_daily(start=date, end=date, market=symbolMarket(var))
        df = df[df['variety'] == var]
        # print(df)
        return df

    if type == 'var':
        df = pd.DataFrame()
        for market in ['DCE','cfe','SHFE','CZCE']:
            df = df.append(get_future_daily(start=date, end=date, market=market))
            df['market'] = market.upper()
            # print(df)
        varList = list(set(df['variety']))
        # print(varList)

        dfL=pd.DataFrame()
        for var in varList:
            try:
                ry = get_mainSubmainMarket(date, var,df = df)
                # ry['market']=df['market']
                # print(ry)
                if ry:
                    dfL = dfL.append(pd.DataFrame([ry], index=[var],columns=['差价','basicPrice(%)','symbol1','symbol2','M-differ','Slope(%)']))

                    # dfL['market']=dfL[dfL['symbol2']==df['symbol2']]#&df['market']
                    # df['market']=dfL

                    # print(dfL)
            except:
                pass
        dfL['date'] = date
        # print(df)
        # dfL2=pd.DataFrame()
        for i in dfL['symbol2'].drop_duplicates():
        #     # print(i)
            df2=df[df['symbol']==i]['market']
            dfL.append(df2)
        # dfL=dfL2.append(dfL)
        #     print(df2)

        # dfL = dfL.sort_values('basicPrice')
        # dfL = dfL[(dfL['basicPrice'] >= 2) | (dfL['basicPrice'] <= -2)]
        # dfL = dfL[dfL['M-differ']<=0]
        dfL['signal'] = np.sign(dfL['Slope(%)'])
        dfL = dfL.sort_values('Slope(%)')

        long = dfL[dfL['signal'] > 0]
        long1 = int(long['signal'].count()/1)
        long = long.tail(long1)

        short = dfL[dfL['signal'] < 0]
        short1 = int(short['signal'].count() / 1)
        short = short.head(short1)

        dfL = long.append(short)#.dropna().drop_duplicates()



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
    # print(symbol1,close1,symbol2,close2)

    A = re.sub(r'\D', '', symbol1)
    A1 = int(A[:-2])
    A2 = int(A[-2:])
    B = re.sub(r'\D', '', symbol2)
    B1 = int(B[:-2])
    B2 = int(B[-2:])

    c = (A1 - B1) * 12 + (A2 - B2)
    # print('sss:',c)
    if close1 == 0 or close2 == 0:
        return False
    if c > 0:
        #做多 (近月-远月)/远月/相差月数*100%
        return close1-close2,round((close1-close2)/close2/c*100,2), symbol1,symbol2,c,round((close2-close1)/((close2+close1)/2)/c*12,2)
    else:
        # 做空 (远月-近月)/远月/相差月数*100%
        return close2-close1,round((close2-close1)/close2/c*100,2), symbol1,symbol2,c,round((close2-close1)/((close2+close1)/2)/c*12,2)#.lower()
        #
        #月差接近3%两月资金炒翻翻，商品保证金一般6%左右，远月向近月靠拢2月资金翻倍


if __name__ == '__main__':
    # data = get_mainSubmainMarket_bar(date='20200817', type='var')
    # print(data)
    # data=get_mainSubmainMarket(date='20201013', var='BU')
    # print(data)

    # 连接数据库u
    client = MongoClient('localhost', 27017)
    db = client.futures34
    cfd = db.basicPrice
    begin = datetime.date(2020, 10, 28)
    end = datetime.date(2020, 10, 28)

    for i in range((end - begin).days + 1):
        # print(i)
        day = begin + datetime.timedelta(days=i)
        days = day.strftime('%Y%m%d')
        # print(days)

        try:
          # data=get_mainSubmainMarket(date,'BU')
            data =get_mainSubmainMarket_bar(date=days, type='var')
            data['date'] = days
            print(data)
            # cfd.insert_many(json.loads(data.T.to_json()).values())
            # print(json.loads(data.T.to_json()).values())
            # print(data)
        except:
            print(days, '数据异常')
            continue

