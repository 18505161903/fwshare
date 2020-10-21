# encoding:utf-8
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plot
import math
#target_url = ("https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data")
#rockVMines = pd.read_csv(target_url ,header=None,prefix="V") #prefix前缀
rockVMines = pd.read_csv('../rockdata.txt',header=None,prefix="V")  #prefix前缀
row2 = rockVMines.iloc[1,0:60]
row3 = rockVMines.iloc[2,0:60]
n = len(row2)
mean2 =  row2.mean()
mean3 =  row3.mean()
t2=0 ; t3=0;t1=0
for i in range(n):
    t2 += (row2[i] - mean2) * (row2[i] - mean2) / n
    t3 += (row3[i] - mean3) * (row3[i] - mean3) / n
r23=0
for i in range(n):
    r23 += (row2[i] - mean2)*(row3[i] - mean3)/(n* math.sqrt(t2 * t3))
print(r23)

corMat = DataFrame(rockVMines.corr())  #corr 求相关系数矩阵
print(corMat)
plot.pcolor(corMat)
plot.show()