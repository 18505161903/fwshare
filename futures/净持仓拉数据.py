import tushare as ts
import pandas as pd
from pymongo import MongoClient
import json
import datetime
import matplotlib.pyplot as plt

client = MongoClient('localhost', 27017)
db = client.futures3
jd = db.jd

pro = ts.pro_api('c0cad8f56caba4e70702d606290d04f88514a6bef046f60d13144151')
df = pro.fut_holding( symbol='JD2006', exchange='DCE'
df2=df.fillna(0)
df2=df2.loc[df2['broker']!='期货公司会员']
print(df2)
jd.insert_many(json.loads(df2.T.to_json()).values())
print(json.loads(df2.T.to_json()).values())

