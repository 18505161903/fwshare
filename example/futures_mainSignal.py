# encoding: utf-8

import pandas as pd
from pandas import DataFrame
import json
from pymongo import MongoClient


pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

client = MongoClient('localhost', 27017)
db = client.futures
market=db.market
position=db.position
mainSignal=db.mainSignal

date='20190101'
market=DataFrame(list(market.find({'date':{'$gte':date}})))
position=DataFrame(list(position.find({'date':{'$gte':date}})))


# 选取条件
# market=market.loc[market['open_interest']>1000]

# 以日期和持仓量2个字段分组筛选唯一主力合约
# 方法一：在分组中过滤出Count最大的行
market=market.groupby(['date','variety']).apply(lambda x: x[x.open_interest==x.open_interest.max()])
# print(market.head())

#方法二：用transform获取原dataframe的index，然后过滤出需要的行
# market1 = market.groupby(['date','variety'])['open_interest'].transform(max)
# market=market1=market['open_interest']
# print(market)
# market = market.groupby(['date','variety'])['open_interest'].agg(max)

#去重交易合约
# market=market.drop_duplicates()
# #价格变化量
market['change'] = market['close'] - market['open']

#删除_id,index,date,variety
market.drop(market.columns[[0,2,4,12]], axis=1,inplace=True)
# marketdata = market.copy()
#
# 净持仓变动量
netPosition=position.groupby(['date','variety'])[['long_openIntr','short_openIntr']].sum()
netPosition['净持仓']=netPosition.apply(lambda x:x['long_openIntr']-x['short_openIntr'],axis=1)
netPosition['上一日净持仓']=netPosition.groupby('variety')['净持仓'].shift(1)
netPosition['净持仓变化量']=netPosition.apply(lambda x: x['净持仓']-x['上一日净持仓'],axis=1)
netPosition=netPosition.dropna().reset_index()
# 两表合并
df=pd.merge(netPosition,market,on=['date', 'variety'],how='outer')

df['交易信号'] = df.apply(lambda x: 0 if x['净持仓变化量']*x['change']>=0  else 1 if x['净持仓变化量']>0 else -1,axis=1)
#删除nan并去重
df=df.dropna().drop_duplicates()

df=pd.DataFrame(df)
# print(df.head())
mainSignal.insert(json.loads(df.T.to_json()).values())
print(json.loads(df.T.to_json()).values())