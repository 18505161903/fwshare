import quandl
import pandas as pd
import json
from pymongo import MongoClient
import datetime

pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

client = MongoClient('localhost', 27017)
db = client.futures
market=db.market
position=db.position
main=db.cftc

quandl.ApiConfig.api_key = '-GGCYDJNb2cxMLTvqTho'

d = pd.read_excel(r'E:\code.xlsx', input_col=0)
ds = d[['品种名称', 'code']]


for temp in d['code']:
    # print(temp)
    try:
        data = quandl.get('CFTC/' + temp + '_F_L_ALL', paginate=True)
        data['code'] = temp
        # data = pd.DataFrame(data[0],columns=list(data['code']))
        # print(data)
        # data = quandl.get('CFTC/' + temp + '_F_L_ALL', start_date='2018-9-1', end_date='2019-09-1')

        # # 净持仓
        data['大户净持仓'] = data.apply(lambda x: x['Noncommercial Long'] - x['Noncommercial Short'], axis=1)
#         # print(data)
        data['套保净持仓'] = data.apply(lambda x: x['Commercial Long'] - x['Commercial Short'], axis=1)
        data['散户净持仓'] = data.apply(lambda x: x['Nonreportable Positions Long'] - x['Nonreportable Positions Short'],
                                   axis=1)
        # print(data)
        # # # 最大值最小值
        chg = data[['大户净持仓', '套保净持仓', '散户净持仓']]
        # print(chg)
        max = chg.rolling(window=156).max().dropna()  # ,min_periods=1
        min = chg.rolling(window=156).min().dropna()  # 156
        # print(min.tail(5))
        # # # #
        hb = pd.merge(max, min, on=['Date'], how='outer')
        hb1 = pd.merge(data, hb, on=['Date'], how='outer')
        # print(hb1)
        # # cot指标
        data['大户cot指标(%)'] = round(
            hb1.apply(lambda x: ((x['大户净持仓'] - x['大户净持仓_y']) / (x['大户净持仓_x'] - x['大户净持仓_y'])) * 100, axis=1), 2)
        data['套保cot指标(%)'] = round(
            hb1.apply(lambda x: ((x['套保净持仓'] - x['套保净持仓_y']) / (x['套保净持仓_x'] - x['套保净持仓_y'])) * 100, axis=1), 2)
        data['散户cot指标(%)'] = round(
            hb1.apply(lambda x: ((x['散户净持仓'] - x['散户净持仓_y']) / (x['散户净持仓_x'] - x['散户净持仓_y'])) * 100, axis=1), 2)

        # data = pd.merge(data, ds, on=['code'], how='outer').dropna().drop_duplicates()

        print(data.tail(10))
    except:
        pass
    continue

print('完成')