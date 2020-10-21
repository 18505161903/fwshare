import pymongo

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["runoobdb"]
# mycol = mydb["sites"]
#
# for x in mycol.find():
#     print(x)


client = pymongo.MongoClient('localhost', 27017)
futures = client["futures"]
mainSignal = futures["mainSignal"]

mainSignal.aggregate([{"$group":{"_id":"$variety","num_tutorial":{"$sum":1}}}])

print(mainSignal)