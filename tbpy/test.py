import pandas as pd
import datetime

from fushare.dailyBar import get_future_daily
from futures.CfdBasis import get_mainSubmainMarket
from futures.CfdBasis import get_mainSubmainMarket_bar

begin = datetime.date(2020, 10, 20)
end = datetime.date(2020, 10, 20)

df = pd.DataFrame()
for i in range((end - begin).days + 1):
    # print(i)
    day = begin + datetime.timedelta(days=i)
    days = day.strftime('%Y%m%d')

    for market in ['dce', 'cffex', 'shfe', 'czce']:
        df = df.append(get_future_daily(start=begin, end=end, market=market))
    varList = list(set(df['variety']))

    for var in varList:
        if var:
            ry = get_mainSubmainMarket(days, var)
            print(ry)
            # if ry:
            #     dfL = dfL.append(pd.DataFrame([ry], index=[var], columns=['差价', 'basicPrice(%)', 'symbol1', 'symbol2', 'M-differ', 'Slope(%)']))
            #     dfL['date'] = days
            #     # print(dfL)
            # symbolList = list(set(dfL['symbol2']))#远月合约
            # for symbol in symbolList:
            #     df=df[['date', 'variety', 'symbol', 'close']]
            #     if symbol:
            #         df1= df[df['symbol'] == symbol]
            #         # dfl=df.append(df1)
            #         print(df1)