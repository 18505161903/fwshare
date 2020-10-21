# encoding: utf-8
# import tensorflow as tf
import quandl
import pandas as pd
from pymongo import MongoClient

pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大列

quandl.ApiConfig.api_key = '-GGCYDJNb2cxMLTvqTho'

d = pd.read_excel(r'E:\code.xlsx', input_col=0)
code = d[['品种简称', 'code']]

data2 = pd.DataFrame()
for temp in d['code']:
    try:
        data = quandl.get('CFTC/' + temp + '_F_L_ALL', paginate=True)
        data['code'] = temp
        # 净持仓
        data['大户净持仓'] = data.apply(lambda x: x['Noncommercial Long'] - x['Noncommercial Short'], axis=1)
        data['套保净持仓'] = data.apply(lambda x: x['Commercial Long'] - x['Commercial Short'], axis=1)
        data['散户净持仓'] = data.apply(lambda x: x['Nonreportable Positions Long'] - x['Nonreportable Positions Short'],
                                   axis=1)
        # 最大值最小值
        chg = data[['大户净持仓', '套保净持仓', '散户净持仓']]
        max = chg.rolling(window=156).max().dropna()
        min = chg.rolling(window=156).min().dropna()

        hb = pd.merge(max, min, on=['Date'], how='outer')
        hb1 = pd.merge(data, hb, on=['Date'], how='outer')
        # cot指标
        data['大户cot(%)'] = round(
            hb1.apply(lambda x: ((x['大户净持仓'] - x['大户净持仓_y']) / (x['大户净持仓_x'] - x['大户净持仓_y'])) * 100, axis=1), 2)
        data['套保cot(%)'] = round(
            hb1.apply(lambda x: ((x['套保净持仓'] - x['套保净持仓_y']) / (x['套保净持仓_x'] - x['套保净持仓_y'])) * 100, axis=1), 2)
        data['散户cot(%)'] = round(
            hb1.apply(lambda x: ((x['散户净持仓'] - x['散户净持仓_y']) / (x['散户净持仓_x'] - x['散户净持仓_y'])) * 100, axis=1), 2)

        data = data[['code', '大户净持仓', '套保净持仓', '散户净持仓', '大户cot(%)', '套保cot(%)', '散户cot(%)']]
        data = data.reset_index()
        data = pd.merge(data, code)
        #         data = data[data['套保cot(%)']>=100 or data['套保cot(%)']<=0]
        data = data.tail(10)
        data2 = data2.append(data)

    except:
        print('??')
    continue

# data2=data2[data2['套保cot(%)']>=100 or data2['套保cot(%)']<=0]
data2
