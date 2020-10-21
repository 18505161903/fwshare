import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from sklearn import metrics
from IPython import display


class ZcSummary:
    # 从CSV文件中读取数据，返回DataFrame类型的数据集合。
    def read_csv(self):
        v_dataframe = pd.read_csv("california_housing_train.csv", sep=",")
        # 打乱数据集合的顺序。有时候数据文件有可能是根据某种顺序排列的，会影响到我们对数据的处理。
        v_dataframe = v_dataframe.reindex(np.random.permutation(v_dataframe.index))
        return v_dataframe

    # 预处理特征值
    def preprocess_features(self, california_housing_dataframe):
        selected_features = california_housing_dataframe[
            ["latitude",
             "longitude",
             "housing_median_age",
             "total_rooms",
             "total_bedrooms",
             "population",
             "households",
             "median_income"]
        ]
        processed_features = selected_features.copy()
        # 增加一个新属性：人均房屋数量。
        processed_features["rooms_per_person"] = (
                california_housing_dataframe["total_rooms"] /
                california_housing_dataframe["population"])
        return processed_features

    # 预处理标签
    def preprocess_targets(self, california_housing_dataframe):
        output_targets = pd.DataFrame()
        # 数值过大可能引起训练过程中的错误。因此要把房价数值先缩小成原来的
        # 千分之一，然后作为标签值返回。
        output_targets["median_house_value"] = (
                california_housing_dataframe["median_house_value"] / 1000.0)
        return output_targets

    # 主函数
    def main(self):
        tf.logging.set_verbosity(tf.logging.ERROR)
        pd.options.display.max_rows = 10
        pd.options.display.float_format = '{:.1f}'.format

        california_housing_dataframe = self.read_csv()
        # 对于训练集，我们从共 17000 个样本中选择前 12000 个样本。
        training_examples = self.preprocess_features(california_housing_dataframe.head(12000))
        training_targets = self.preprocess_targets(california_housing_dataframe.head(12000))
        # 对于验证集，我们从共 17000 个样本中选择后 5000 个样本。
        validation_examples = self.preprocess_features(california_housing_dataframe.tail(5000))
        validation_targets = self.preprocess_targets(california_housing_dataframe.tail(5000))

        # 展示数据集的概要情况。
        print("Training examples summary:")
        display.display(training_examples.describe())
        print("Validation examples summary:")
        display.display(validation_examples.describe())

        print("Training targets summary:")
        display.display(training_targets.describe())
        print("Validation targets summary:")
        display.display(validation_targets.describe())


t = ZcSummary()
t.main()

