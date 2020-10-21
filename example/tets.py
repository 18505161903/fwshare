import pymongo
import pandas as pd
from pandas import Series,DataFrame
import matplotlib as plt
import matplotlib.dates as mdate
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
#二行即可搞定画图中文乱码
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

#连接数据库
client = pymongo.MongoClient('localhost',27017)
print(client)
futures = client.futures
marketdata = futures.marketdata
# unit = futures.unit
position = futures.position


# df = DataFrame(list(position.find({'date': {'$gte': '20070523'}})))
trade = position.find_one({'date': '20020107', 'variety': 'CU'})['vol']
print(trade)
# date='20180101'
# #加载数据
# position = DataFrame(list(position.find({'date': {'$gte': date}})))
# marketdata = DataFrame(list(marketdata.find({'date': {'$gte': date}})))
# #主力合约



# #替换空值为0
# # clean_z = marketdata['open_interest'].fillna(0)
# # clean_z[clean_z==''] = '0'
# # marketdata['open_interest'] = clean_z
# # 字段类型转换
# marketdata['open_interest'] = marketdata['open_interest'].astype('int')
# #选取条件
# marketdata=marketdata.loc[marketdata['open_interest']>1000]
# #以日期和持仓量2个字段分组筛选唯一主力合约
# marketdata=marketdata.groupby(['date','variety']).apply(lambda x: x[x.open_interest==x.open_interest.max()])
# #去重交易合约
# marketdata=marketdata.drop_duplicates()
# #价格变化量
# # marketdata['change'] = marketdata['close'] - marketdata['open']
# marketdata = marketdata.copy()
# print(marketdata.head())
#
# #净持仓变动量
# netPosition=position.groupby(['date','variety'])[['long_openIntr','short_openIntr']].sum()
# netPosition['净持仓']=netPosition.apply(lambda x:x['long_openIntr']-x['short_openIntr'],axis=1)
# netPosition['上一日净持仓']=netPosition.groupby('variety')['净持仓'].shift(1)
# netPosition['净持仓变化量']=netPosition.apply(lambda x: x['净持仓']-x['上一日净持仓'],axis=1)
# netPosition=netPosition.dropna().reset_index()
# print(netPosition.head())
#
# # #净持仓，价格变化量合并
# df=pd.merge(netPosition,marketdata,on=['date', 'variety'],how='outer')
# df['交易信号'] = df.apply(lambda x: 0 if x['净持仓变化量']*x['change']>=0  else 1 if x['净持仓变化量']>0 else -1,axis=1)
# print(df.head())