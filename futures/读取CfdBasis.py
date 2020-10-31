import pandas as pd
import datetime

from fushare.dailyBar import get_future_daily
from futures.CfdBasis import get_mainSubmainMarket
from futures.CfdBasis import get_mainSubmainMarket_bar
import numpy as np

begin = datetime.date(2020, 10, 20)
end = datetime.date(2020, 10, 30)


for i in range((end - begin).days + 1):
    day = begin + datetime.timedelta(days=i)
    days = day.strftime('%Y%m%d')

    df= pd.DataFrame()
    for market in ['dce', 'cffex', 'shfe', 'czce']:
        df = df.append(get_future_daily(start=begin, end=end, market=market))
    varList = list(set(df['variety']))

    dfL = pd.DataFrame()
    for var in varList:
        try:
            ry = get_mainSubmainMarket(days, var)
            # print(ry)
            if ry:
                dfL = dfL.append(pd.DataFrame([ry], index=[var], columns=['差价', 'basicPrice(%)', 'symbol1', 'symbol2', 'M-differ', 'Slope(%)']))
                # print(dfL)
        except:
            pass

    dfL['date'] = days
    symbolList = list(set(dfL['symbol2']))#远月合约
    # print(symbolList)

    dfl=pd.DataFrame()
    for symbol in symbolList:
        # print(symbol)
        df=df[['date', 'variety', 'symbol', 'open','close']]
        if symbol:
            df1= df[df['symbol'] == symbol]
            # print(df1)
            dfl=dfl.append(df1)
            print(dfl)

    # df2=pd.DataFrame()
    #
    # mainSubmainMarket = get_mainSubmainMarket_bar(date=days, type='var')
    # # mainSubmainMarket['date']=days
    # mainSubmainMarket=df2.append(mainSubmainMarket)
    # mainSubmainMarket['date']=days
    # mainSubmainMarket = mainSubmainMarket.reset_index()
    # mainSubmainMarket = mainSubmainMarket.rename(columns={'index': 'variety', 'symbol2': 'symbol'})
    #
    # data=pd.merge(dfl,mainSubmainMarket,on=['date','variety','symbol'], how='outer').fillna(0)
    #
    # data=data.to_excel(r'D:\PyFile\CfdBasis.xlsx',index=False)
    # print(data)






    # df3 = pd.DataFrame()
    # df3['close'] = data['close']  # 收盘价
    # df3['change'] = df3['close'] - df3['close'].shift(1)  # 当日涨跌
    # # df3=df3.dropna()#抛弃nan数据
    # print(df3)

    #计算持仓
    # df3['pos']=0
    # df3['pos'][np.sign(df3['change'])]=100000???

    #计算每日盈亏和手续费
    # df3['pnl']=df3['change']+df['pos']#盈亏
    # df['fee']=0#手续费
    # df['fee'][df['pos']!=df['pos'].shift(1)]=df['close']*20000*0.0003
    # df['netpnl']=df['pnl']-df['fee']#净盈亏

    #汇总求和盈亏，绘制资金曲线
    # df['cumpnl']=df['netpnl'].cumsum()
    # df['cumpnl'].plot()







