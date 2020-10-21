import tushare as ts
import pandas as pd
from pymongo import MongoClient
import fushare,json

pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

client = MongoClient('localhost', 27017)


pro = ts.pro_api('c0cad8f56caba4e70702d606290d04f88514a6bef046f60d13144151')

var=fushare.get_mainSubmain_bar(type = 'var')
var=var['symbol']
print(var)
for vars in var:
    try:
        df = pro.fut_holding(symbol=vars)
        print(df)
        df2=df.fillna(0)
        df2=df2.loc[df2['broker']!='期货公司会员']
        print(df2)
        # mainSubmainPosition.insert_many(json.loads(df2.T.to_json()).values())
        # print(json.loads(df2.T.to_json()).values())
    except:
        pass


