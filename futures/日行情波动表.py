# encoding: utf-8
import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt

pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

pro = ts.pro_api('c0cad8f56caba4e70702d606290d04f88514a6bef046f60d13144151')
df = pro.fut_daily( symbol='JD2006', exchange='DCE')
df=df.sort_values(['trade_date'],ascending=True)
print(df)
# df2=df.fillna(0)
# jd=df2.loc[df2['broker']!='期货公司会员']
# jd=jd.copy()
# broker2=['宏源期货','方正中期','英大期货','美尔雅期货','格林大华']
# jd['净持仓']=jd.apply(lambda x: x['long_hld'] - x['short_hld'], axis=1)
# jd=jd[jd['trade_date']>='20200310']
#
# net_position = jd.groupby(['trade_date', 'symbol'])['净持仓'].sum().reset_index(name='净空汇总')
# sums = jd.copy()
# # sums = sums[sums['symbol']=='JD2005']
# times = sums[sums['trade_date'] == sums['trade_date'].iloc[-1]]
# # print(times)
# brokers = times['broker']
# df = pd.DataFrame()
# for i in brokers:
#     broker = [sums[sums['broker'] == i]]
#     df = df.append(broker)
#
# df['净变动'] = df['净持仓'] - df['净持仓'].shift(1).fillna(0)
# # print(df)
# df = df[df['trade_date'] == df['trade_date'].iloc[-1]]
# sums = df.sort_values('净持仓')
# sums = sums[sums['净持仓'] != 0]
# sums =sums[['trade_date', 'symbol','broker','净持仓','净变动','vol','vol_chg','long_hld','long_chg','short_hld','short_chg']]
# print(sums)
#
#
#
# sort=sums.sort_values('净持仓',inplace=False)
# plt.bar(range(len(sort['净持仓'])),sort['净持仓'])
# plt.xticks(range(len(sort['broker'])),sort['broker'],rotation='vertical')
# # plt.xlabel('品种')
# plt.ylabel('净持仓')
# plt.title(' 净空排名 '+sort['trade_date'].iloc[0])
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# plt.show()