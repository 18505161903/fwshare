import json
import pandas as pd
import pymongo

# 连接数据库
client = pymongo.MongoClient('localhost', 27017)
futures = client.futures
df2=pd.read_csv(r'E:\fit.csv',',',encoding='gbk')
df = pd.DataFrame(df2)
df=df.dropna().drop_duplicates()
futures.mainSignal.insert_many(json.loads(df.T.to_json()).values())
print(json.loads(df.T.to_json()).values())