import json
from pymongo import MongoClient
import pandas as pd


if __name__=='__main__':

    # 连接数据库
    client = MongoClient('localhost', 27017)
    futures = client.futures2

    data = pd.read_excel(r'e:\unit.xlsx',input_col=0)
    df = pd.DataFrame(data)
    futures.unit.insert(json.loads(df.T.to_json()).values())
    print(json.loads(df.T.to_json()).values())

    # # encoding: utf-8
    #
    # from opendatatools import futures
    # import datetime
    # import os
    # import json
    # from pymongo import MongoClient
    # import pandas as pd

    # if __name__ == '__main__':
    #
    #     markets = ['SHF','CZC', 'DCE']#, 'SHF','CZC', 'DCE', 'CFE'
    #     # 连接数据库
    #     client = MongoClient('localhost', 27017)
    #     db = client.futures
    #     position = db.position
    #
    #     if os.path.exists(r"c:\FuturesPosition.csv"):
    #         os.remove(r"c:\FuturesPosition.csv")
    #     for market in markets:
    #         begin = datetime.date(2018, 11, 8)
    #         end = datetime.date(2018, 11, 9)
    #         for i in range((end - begin).days + 1):
    #             day = begin + datetime.timedelta(days=i)
    #             days=day.strftime('%Y-%m-%d')
    #             print(days)
    #             try:
    #                 df, msg = futures.get_trade_rank(market, date=days)
    #                 print(days,market)
    #                 #position.insert(json.loads(df.T.to_json()).values())
    #                 # print(json.loads(df.T.to_json()).values())
    #             except:
    #                 print(days,market,'数据异常')
    #                 continue
    #             if os.path.exists(r"c:\FuturesPosition.csv"):
    #                 df.to_csv(r"c:\FuturesPosition.csv",mode='a',encoding='ANSI',header=False)
    #             else:
    #                 df.to_csv(r"c:\FuturesPosition.csv",encoding='ANSI')
    #     data = pd.read_csv(r'c:\FuturesPosition.csv',encoding = "ANSI")
    #     df = pd.DataFrame(data)
    #     position.insert(json.loads(df.T.to_json()).values())
    #     print(json.loads(df.T.to_json()).values())
