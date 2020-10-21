# encoding: utf-8
import pandas as pd
import pymongo
from pandas import DataFrame
import matplotlib.pyplot as plt
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行


client = pymongo.MongoClient('localhost', 27017)
futures = client.futures2
market = futures.market2

start = '20190101'
end ='20200306'
var1 = 'OI'
var2 = 'Y'
print(var1)
market1 = DataFrame(list(market.find({'date': {'$gte': start}, 'variety': var1}))).drop_duplicates(['date','variety','symbol'], 'last')
market2 = DataFrame(list(market.find({'date': {'$gte': start}, 'variety': var2}))).drop_duplicates(['date','variety','symbol'], 'last')
print(market1.head())


# 指数收盘
market1['cv'] = market1.apply(lambda x: x['close'] * x['open_interest'], axis=1)
market1 = market1.groupby(['date', 'variety'])[['cv', 'open_interest']].sum()
market1[var1] = market1['cv'] / market1['open_interest']
market1 = market1[var1].reset_index()

# 指数收盘
market2['cv'] = market2.apply(lambda x: x['close'] * x['open_interest'], axis=1)
market2 = market2.groupby(['date', 'variety'])[['cv', 'open_interest']].sum()
market2[var2] = market2['cv'] / market2['open_interest']
market2 = market2[var2].reset_index()

#两表合并
merge = pd.merge(market1,market2, on=['date'], how='left')
merge = merge[['date',var1,var2]]
merge['差价'] = merge.apply(lambda x: x[var1] - x[var2], axis=1)
print(merge.tail(20))

# 画图
merge = merge.set_index('date')
with pd.plotting.plot_params.use('x_compat', True):  # 方法一
    merge[['差价']].plot(color='r', title=start +'  '+ end  +' '+var1+var2+' 价差：'+str(int(merge['差价'].iloc[-1])))
    # mergee['today_net'].plot(secondary_y=['today_net'])
    # mergee.ylabel('净持仓')

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.show()