# import  matplotlib.pyplot as plt
# from sklearn import linear_model
# import numpy as np
import pandas as pd
# datasets_X = []
# datasets_Y = []
# fr = open('e:\signal.csv','r')

# lines = fr.readlines()
# # for line in lines:
# #     # items = line.strip().split(',')
# #     datasets_X.append(int(items[0]))
# #     datasets_Y.append(int(items[1]))
# length = len(datasets_X)
# datasets_X = np.arry(datasets_X).reshape([length,1])
# datasets_Y = np.arry(datasets_Y)
# minX = min(datasets_X)
# maxX = max(datasets_X)
# X = np.arange(minX,maxX).reshape([-1,1])
#
# linear = linear_model.LinearRegression()
# linear.fit(datasets_X,datasets_Y)
# plt.scatter(datasets_X,datasets_Y,color = 'red')
# plt.plot(X.linear.predict(X),color = 'blue')
# plt.ylabel('Price')
# plt.show()

df = pd.read_csv(r'e:\signal.csv',encoding = "ANSI",parse_dates=['date'], index_col='date')
# df['date'] = pd.to_datetime(df['date'])
print("s")