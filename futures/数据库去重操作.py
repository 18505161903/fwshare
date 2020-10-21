db.getCollection('position').aggregate([
    {
        $group: { _id: {date: '$date',variety: '$variety',symbol:'$symbol',long_party_name:'$long_party_name'},count: {$sum: 1},dups: {$addToSet: '$_id'}}
    },
    {
        $match: {count: {$gt: 1}}
    }
],{allowDiskUse:true}).forEach(function(doc){
    doc.dups.shift();                       // 去除重复组的第一个元数据_id，得到除第一个之外的其他元组
    db.position.remove({_id: {$in: doc.dups}}); // remove()删除这些重复的数据
})



# position.aggregate([
#     {
#         $group: { _id: {date: '$date',variety: '$variety'},count: {$sum: 1}}},{$match:{count:{$gt:1}}}])
# ]).forEach(function(doc){
#     doc.dups.shift();
#     db.userInfo.remove({_id: {$in: doc.dups}});
# })
#
#
# # futures.getCollection('market').aggregate([
# #     {
# #         $group: { _id: {userName: '$userName',age: '$age'},count: {$sum: 1},dups: {$addToSet: '$_id'}}
# #     },
# #     {
# #         $match: {count: {$gt: 1}}
# #     }
# # ]).forEach(function(doc){
# #     doc.dups.shift();
# #     db.userInfo.remove({_id: {$in: doc.dups}});
# # })
#
#
#
# db.getCollection('market').aggregate([
#     {
#         $group: { _id: {date: '$date',variety: '$variety'},count: {$sum: 1},dups: {$addToSet: '$_id'}}
#     },
#     {
#         $match: {count: {$gt: 1}}
#     }
# ]).forEach(function(doc){
#     doc.dups.shift();
#     db.userInfo.remove({_id: {$in: doc.dups}});
# })