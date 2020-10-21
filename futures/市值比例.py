import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import json
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
unit = futures.unit
position = futures.position

begin = DataFrame(list(market.find({}).sort([('_id', -1)]).limit(1)))
begin = begin['date'][0]
print(begin)
date = begin
#查询会员
# BrokerID='海通期货'
BrokerID='永安期货'
# BrokerID='徽商期货'
# BrokerID='浙商期货'
#加载数据
market = DataFrame(list(market.find({'date': {'$gte': date}})))
unit = DataFrame(list(unit.find()))
position = DataFrame(list(position.find({'date': {'$gte': date}}))).dropna()

# #选择需要显示的字段
market = market.copy()
# 指数收盘
market['cv'] = market.apply(lambda x: x['close'] * x['open_interest'], axis=1)
closes = market.groupby(['date', 'variety'])[['cv', 'open_interest']].sum()
#待解决问题：根据最小价位变动，给收盘价做五舍四入处理
closes['close_index'] = closes['cv'] / closes['open_interest']
market = closes.reset_index()[['date','variety','close_index']]

unit=unit[[ 'variety','unit']]

# #汇总合约
data3=position[(position['long_party_name'] == BrokerID)]
data3=data3[['date','variety','long_party_name','long_openIntr']]
data3=data3.groupby(['date','variety','long_party_name'])[['long_openIntr']].sum()
print(data3)

data4=position[(position['short_party_name'] == BrokerID)]
data4=data4[['date','variety','short_party_name','short_openIntr']]
data4=data4.groupby(['date','variety','short_party_name'])[['short_openIntr']].sum()
print(data4)

# #并集
data5=pd.merge(data3,data4, on=['date','variety'],how='outer')

data5['会员简称']=data5.apply(lambda x: BrokerID,axis=1)
data5.tail(100)

#nan缺失值填充fillna()为0
data5=data5.fillna(0)

data5['净持仓']=data5.apply(lambda x: x['long_openIntr']-x['short_openIntr'],axis=1)

# df['当日涨幅']=df.apply(lambda x: x['收盘']-x['收盘'].shift(1)-1,axis=1)
#选择需要显示的字段
data5=data5[['会员简称','long_openIntr','short_openIntr','净持仓']]
data5=data5.reset_index(['variety','date'])
netpostion=data5.set_index('date')


netpostion=data5.pivot_table('净持仓',index='date',columns='variety',fill_value=0)
# print(netpostion)
#合约价值
contractValue=pd.merge(market,unit,how='left',sort=False).drop_duplicates()

contractValue['contractValue'] = contractValue.apply(lambda x: x['close_index']*x['unit'],axis=1)
contractValue=contractValue[['date','variety','contractValue']].fillna(0)

# #值替换replace()
# # contractValue=contractValue.replace(['TA'],'PTA')
sz=pd.merge(data5,contractValue,on=['date','variety'],how='left')

# #净持仓价值
sz['净持仓价值']=sz.apply(lambda x: x['净持仓']*x['contractValue']/10000,axis=1)
sznet=sz[['date','variety','会员简称','净持仓价值']]
sz=sznet.sort_values(by='净持仓价值')
sz=sz.pivot_table('净持仓价值',index=['date','会员简称'],columns='variety',fill_value=0)
sz=sz.copy()
# sz['化工板块']=sz[['RU','MA','V','L','PP','BU','TA']].sum(axis=1)
# sz['油脂板块']=sz[['Y','P','OI']].sum(axis=1)
# sz['有色板块']=sz[['CU','AL','ZN','NI','PB']].sum(axis=1)
# sz['黑色板块']=sz[['RB','HC','ZC','J','JM','I']].sum(axis=1)
# sz['黄金白银']=sz[['AU','AG']].sum(axis=1)
# sz['工业品']=sz[['CU','AL','ZN','NI','PB','RB','FG','RU','L','V','TA','MA','PP','JM','J','ZC','I','BU','HC','SM','SF','FU']].sum(axis=1)
# sz['农产品']=sz[['A','C','M','RM','Y','P','OI','CF','SR','JD','CS','AP']].sum(axis=1)
# sz['商品板块']=sz.sum(axis=1)


# chemical=sz.copy()
# chemical=chemical[['RU','MA','V','L','PP','BU','TA','商品板块','工业品','化工板块']]
# chemical['max']=chemical[['RU','MA','V','L','PP','BU','TA']].idxmax(axis=1)
# chemical['min']=chemical[['RU','MA','V','L','PP','BU']].idxmin(axis=1)
# chemical['20200120':]
# chemical = chemical.reset_index()

# # futures = client.futures
# # flows = futures.chemical
# # flows.insert(json.loads(chemical.T.to_json()).values())
print("计算完毕")


net = sznet.copy()

net = net[net['date']==date]
print(net)
sum_chg = net['净持仓价值'].apply(lambda x:abs(x)).sum()
net_position= net['净持仓价值'].apply(lambda x:x).sum()
print('总净持仓价值',sum_chg)

net['比例(%)'] = sznet.groupby(['date', 'variety', '会员简称'])['净持仓价值'].apply(lambda x: (x / sum_chg) * 100)
print(net.sort_values('净持仓价值'))

sort=net.sort_values('比例(%)',inplace=False)
plt.bar(range(len(sort['比例(%)'])),sort['比例(%)'])
plt.xticks(range(len(sort['variety'])),sort['variety'])
# plt.xlabel('品种')
plt.ylabel('净持仓价值比例')
plt.title(BrokerID+' 资金分布 '+sort['date'].iloc[0]+" 总市值："+str(int(sum_chg))+" 净持仓市值："+str(int(net_position)))
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.show()