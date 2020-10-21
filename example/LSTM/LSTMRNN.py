import pandas
import matplotlib.pyplot as plt
dataset = pandas.read_csv('http-request.csv', usecols=[1], engine='python')
plt.plot(dataset)
plt.show()