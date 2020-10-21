# encoding: utf-8
import pandas as pd
from pandas import *
import numpy as np
from pymongo import MongoClient
import matplotlib.pyplot as plt

pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

client = MongoClient('localhost', 27017)
db = client.futures3
jd= db.jd

start='20191107'
broker2=['宏源期货','方正中期','英大期货','美尔雅期货','格林大华']

jd = DataFrame(list(jd.find({'trade_date': {'$gte': start}})))
# print(jd)
# jd=jd.loc[jd['broker']!='期货公司会员']
jd['净持仓']=jd.apply(lambda x: x['long_hld'] - x['short_hld'], axis=1)
jd=jd[jd['净持仓']<0]
# print(jd)
sums =jd.groupby(['trade_date', 'symbol'])['净持仓'].sum().reset_index(name='净空汇总')

df=pd.DataFrame()
for i in broker2:
    try:
        brokers = jd[jd['broker'] == i]
        df2=pd.DataFrame(brokers)
        df = df.append(df2)
    except:
        pass
sums2 = df.groupby(['trade_date', 'symbol'])['净持仓'].sum().reset_index(name='五少净空')
merge = pd.merge(sums2, sums, on=['trade_date', 'symbol'], how='outer').fillna(0)
merge['五少占比']=merge.apply(lambda x: x['五少净空']/x['净空汇总'], axis=1)
merge=merge[merge['symbol']=='JD2005']
print(merge)

# 画图
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

a= pd.DataFrame({'五少占比':np.array(merge['五少占比']),'五少净空':np.array(merge['五少净空'])},index=merge['trade_date'])
ax = a.plot(
    secondary_y=['五少净空'],
    x_compat=True,
    grid=True)

ax.set_title("五少占比-净空")
ax.set_ylabel('占比')
ax.grid(linestyle="--", alpha=0.3)

ax.right_ax.set_ylabel('净空')
plt.show()