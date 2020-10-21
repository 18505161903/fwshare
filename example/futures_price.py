
# encoding: utf-8

from opendatatools import futures
import datetime
import os
import pandas as pd
import math
import tushare as ts
import datetime
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行



if __name__ == '__main__':

    if os.path.exists(r"c:\price.csv"):
        os.remove(r"c:\price.csv")

    begin = datetime.date(2018, 10, 25)
    end = datetime.date(2018, 10, 25)
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        days = day.strftime('%Y-%m-%d')
        dce = ts.get_dce_daily(days)
        shf = ts.get_shfe_daily(days)
        zce = ts.get_czce_daily(days)
        cff = ts.get_cffex_daily(days)
        frames = [dce, shf, zce, cff]
        try:
            df2 = pd.concat(frames)
            #print(df2)
            df2 = df2.dropna(axis=0, how='any')
            df2['close'] = df2['close'].astype(float)
            df2['test'] = df2['close'] * df2['volume']
            print(df2.head())
            df2 = df2.groupby('variety')['volume', 'test'].sum()
            df2['set_close'] = round(df2['test'] / df2['volume'])
            df2['date'] = days
            df2 = df2.dropna(axis=0, how='any')
            df2 = df2.reset_index()
            df2 = df2[['date', 'variety', 'set_close']]
        except:
            print(days, frames, '数据异常')
            continue
        if os.path.exists(r"c:\price.csv"):
            df2.to_csv(r"c:\price.csv", mode='a', encoding='ANSI', header=False)
        else:
            df2.to_csv(r"c:\price.csv", encoding='ANSI')










