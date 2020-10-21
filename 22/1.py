#-*- coding:utf-8 -*-

import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient('localhost')
# client = MongoClient('localhost', 27017)
db = client.futures
market = db.market

#数据库中删除重复的数据
def save_to_mongo(market):
    market['host_info_new'].update({'variety': market['variety'], 'date': market['date']}, {'$set': market}, True)
    # print(market)
if __name__ == '__main__':
    pool = Pool()
    s=pool.map(save_to_mongo, [market for market in db['host_info_old'].find()])
    #
    # s=[market for market in db['host_info_old'].find()]
    print(s)