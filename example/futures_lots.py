import json
from pymongo import MongoClient
import pandas as pd


if __name__=='__main__':

    # 连接数据库
    client = MongoClient('localhost', 27017)
    futures = client.futures

    data = pd.read_excel(r'c:\lots.xlsx',input_col=0)
    df = pd.DataFrame(data)
    futures.lots.insert(json.loads(df.T.to_json()).values())
    print(json.loads(df.T.to_json()).values())