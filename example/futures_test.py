import pymongo
import pandas as pd
import matplotlib as plt
from pandas import Series,DataFrame
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

#连接数据库
client = pymongo.MongoClient('localhost',27017)
futures = client.futures


market = futures.market
unit = futures.unit
position = futures.position
#加载数据
market = DataFrame(list(market.find()))
unit = DataFrame(list(unit.find()))
position = DataFrame(list(position.find()))


# #类型转换
# market['set_close'] = market['set_close'].astype(float)
# unit['unit'] = unit['unit'].astype(float)

#大写字母
position['variety']=position['variety'].str.upper()

#删除/选取某行含有特殊数值的列
position=position.set_index('名次')

#选择需要显示的字段
data1=market[['date','variety','set_close']]

data2=unit[[ 'variety','unit']]
position=position[['date','variety','symbol','持买仓量期货公司','持买仓量', '持买仓量增减','持卖仓量期货公司','持卖仓量', '持卖仓量增减']]
# print(position.head())

#查询会员
members='永安期货'
data3=position[(position['持买仓量期货公司'] == members)]
#汇总合约
data3=data3[['date','variety','持买仓量期货公司','持买仓量']]
data3=data3.groupby(['date','variety','持买仓量期货公司'])[['持买仓量']].sum()
data4=position[(position['持卖仓量期货公司'] == members)]
# print(data4.head())
data4=data4[['date','variety','持卖仓量期货公司','持卖仓量']]
data4=data4.groupby(['date','variety','持卖仓量期货公司'])[['持卖仓量']].sum()
# print(data3)
# print(data4)
#并集
data5=pd.merge(data3,data4, on=['date','variety'],how='outer')
data5['会员简称']=data5.apply(lambda x: members,axis=1)
#nan缺失值填充fillna()为0
data5=data5.fillna(0)
data5['净持仓']=data5.apply(lambda x: x['持买仓量']-x['持卖仓量'],axis=1)
#选择需要显示的字段
data5=data5[['会员简称','持买仓量','持卖仓量','净持仓']]
data5=data5.reset_index(['variety','date'])
# print(data5)

#合约价值
contractValue=pd.merge(data1,data2,how='left',sort=False).drop_duplicates()
contractValue['contractValue'] = contractValue.apply(lambda x: x['set_close']*x['unit'],axis=1)
contractValue=contractValue[['date','variety','contractValue']]
#值替换replace()
# contractValue=contractValue.replace(['TA'],'PTA')
print(contractValue)
# contractValue.set_index(['date','variety'], inplace = True)
sz=pd.merge(data5,contractValue,on=['date','variety'],how='left')
#净持仓价值
sz['净持仓价值']=sz.apply(lambda x: x['净持仓']*x['contractValue'],axis=1)
sz=sz[['date','variety','会员简称','净持仓价值']]
sz=sz[sz['date']=='2018-10-23']
# print(sz)

sz=sz.sort_values(by='净持仓价值')
# print(sz)
sz.plot.bar(x='variety',y='净持仓价值',figsize=(20,16),label=members)
# print(sz['净持仓价值'].sum())

long=sz[sz['净持仓价值']>1e+09]
short=sz[sz['净持仓价值']<-1e+09]
# print(long,short)

#二行即可搞定画图中文乱码
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

# sz=sz.set_index(['date','variety'])
# print(sz.rank(method="max",ascending=True))

