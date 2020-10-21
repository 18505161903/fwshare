import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import json

import datetime
import time
from pandas import Series,DataFrame
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行
#二行即可搞定画图中文乱码
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
from IPython.core.display import display, HTML

#连接数据库
client = pymongo.MongoClient('localhost',27017)
futures = client.futures2

market = futures.market


begin = DataFrame(list(market.find({}).sort([('_id', -1)]).limit(1)))
begin = begin['date'][0]
print(begin)

symbol = DataFrame(list(market.find({'date': begin})))
symbol = symbol['symbol']

df = pd.DataFrame()

for var in symbol:
    try:
        market_symbol = DataFrame(list(market.find({'symbol': var, 'date': {'$gte': '20190501'}})))
        # print(market_symbol)
        # market_symbol = market_symbol[market_symbol['date']<'20190101']
        high = market_symbol['high'].max()
        low = market_symbol['low'].min()
        close = market_symbol['close'].iloc[-1]
        if len(var) > 8:
            break
        今日幅度 = 0
        # if close>low and low>0:
        #     今日幅度 = (close/low-1)*100
        if high > close and low > 0:
            今日幅度 = (close / high - 1) * 100
        elif close == high:
            今日幅度 = 0
        elif low > 0:
            今日幅度 = (close / high - 1) * 100

        print(close, var)
        dict_symbol = {'date': [begin], 'symbol': [var], 'High': [high], 'Low': [low], 'close': [close], '今日幅度': 今日幅度}
        df1 = pd.DataFrame(dict_symbol)
        df = df.append(df1)
    except:
        continue




df = df[df['今日幅度']<-25].sort_values('今日幅度')
print(df)
df=df.sort_values('今日幅度',inplace=False)
plt.bar(range(len(df['今日幅度'])),df['今日幅度'])
plt.xticks(range(len(df['symbol'])),df['symbol'])
# plt.xlabel('品种')
plt.ylabel('今日幅度')
plt.title(' 涨跌排名 '+df['date'].iloc[0])
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.show()


