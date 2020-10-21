# def delete_single_database_repeat_data():
# 	import pymongo
# 	client = pymongo.MongoClient('localhost', 27017)
# 	db=client.futures2 #这里是将要清洗数据的数据库名字
# 	for table in  db.collection_names():
# 		print 'table name is ',table
# 		collection=db[table]
# 		for url in collection.distinct('gif_url'):#使用distinct方法，获取每一个独特的元素列表
# 			num= collection.count({"gif_url":url})#统计每一个元素的数量
# 			print num
# 			for i in range(1,num):#根据每一个元素的数量进行删除操作，当前元素只有一个就不再删除
# 				print 'delete %s %d times '% (url,i)
# 				#注意后面的参数， 很奇怪，在mongo命令行下，它为1时，是删除一个元素，这里却是为0时删除一个
# 				collection.remove({"gif_url":url},0)
# 			for i in  collection.find({"gif_url":url}):#打印当前所有元素
#                 print(i)


# encoding: utf-8
import pymongo, json
import pandas as pd
from pandas import DataFrame
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

client = pymongo.MongoClient('localhost', 27017)
futures = client.futures2
p=futures.position
m=futures.market

unit=futures.unit
unit=DataFrame(list(unit.find()))
start='20200213'
end='20200213'
mem='一德期货'
var='I'

position = futures.position
position = DataFrame(list(position.find({'date': '20200213','variety': var,'short_party_name':mem})))
print(position)

# for var in unit['variety']:
#     try:
#         position = futures.position
#         position = DataFrame(list(position.find({'variety':var})))
#         # position = DataFrame(list(position.find()))
#         position=position[['symbol','vol_party_name','vol','vol_chg','long_party_name','long_openIntr','long_openIntr_chg','short_party_name','short_openIntr','short_openIntr_chg','variety','date']]
#         position.sort_values('date', inplace=False)
#         position=position.drop_duplicates()

#         p.insert_many(json.loads(position.T.to_json()).values())
#         print(json.loads(position.T.to_json()).values())
#         # print(position.head())
#     except:
#         print('数据异常')
#         continue