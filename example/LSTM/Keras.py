# 简易多层感知神经网络示例
from keras.models import Sequential
from keras.layers import Dense
from pandas import DataFrame
from pymongo import MongoClient
import pandas as pd
import numpy

# 连接数据库
# client = MongoClient('localhost', 27017)
# db = client.futures
# mainSignal = db.mainSignal
# mainSignal=DataFrame(list(mainSignal.find({"variety":"RM"})))
# del mainSignal["_id"]
# del mainSignal["variety"]
# del mainSignal["symbol"]
# mainSignal = mainSignal.rename(columns={'净持仓': 'netPosition', '上一日净持仓': 'pre_netPosition', '净持仓变化量': 'netchange', '交易信号': 'signal'})
# mainSignal = mainSignal.apply(pd.to_numeric, errors="ignore")
# mainSignal.to_csv("mainSignal.csv")

# 加载，预处理数据集

dataset = numpy.loadtxt("mainSignal.csv", delimiter=",")
X = dataset[:,0:8]
Y = dataset[:,8]
# 1. 定义模型
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# 2. 编译模型
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# 3. 训练模型
history = model.fit(X, Y, nb_epoch=100, batch_size=10)
# 4. 评估模型
loss, accuracy = model.evaluate(X, Y)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))
# 5. 数据预测
probabilities = model.predict(X)
predictions = [float(round(x)) for x in probabilities]
accuracy = numpy.mean(predictions == Y)
print("Prediction Accuracy: %.2f%%" % (accuracy*100))