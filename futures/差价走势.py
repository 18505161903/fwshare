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
market = futures.market3

start = '20150105'
end ='20200811'
var1 = 'JD2001'
var2 = 'JD1910'

market1 = DataFrame(list(market.find({'date': {'$gte': start}, 'symbol': var1}))).drop_duplicates(['date','variety','symbol'], 'last')
market2 = DataFrame(list(market.find({'date': {'$gte': start}, 'symbol': var2}))).drop_duplicates(['date','variety','symbol'], 'last')

# 主力收盘
market1[var1] = market1['close']
# 次主力收盘
market2[var2] = market2['close']

#两表合并
merge = pd.merge(market1,market2, on=['date'], how='left')
merge = merge[['date',var1,var2]]
merge['差价'] = merge.apply(lambda x: x[var1] - x[var2], axis=1)
print(merge.tail(20))

# 画图
merge = merge.set_index('date')
with pd.plotting.plot_params.use('x_compat', True):
    merge[['差价']].plot(color='r', title=start +'  '+ end  +' '+var1+' ' + var2+' 差价： '+str(merge['差价'].iloc[-1]))
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.show()