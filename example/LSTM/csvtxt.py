# import pandas as pd
# data = pd.read_csv('E:\rbindex2019.csv',sep='\s+')
# print(data)

##data.to_csv('e:\data.txt', sep='\t', index=False)


import pandas as pd
#
# df =pd.read_csv('E:\rbindex2019.csv',index=False')		# 使用pandas模块读取数据
# print('开始写入txt文件...')
df=pd.read_csv('E:\rbindex2019.csv', header='infer', sep=',', index=False)		# 写入，逗号分隔
print(df)
