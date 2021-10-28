import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from Job import Job
import datetime
import time


class MlModel:
    def __init__(self):
        self.rf = RandomForestRegressor(n_estimators=225, max_features=0.7, random_state=15)

    def train(self):
        data_df = pd.read_csv('./input/data_v3_2.csv', index_col=0)
        data_df = data_df[
            ['YieldScopePriority_X', 'YieldScopePriority_Y', 'IsYieldForEnabled', 'IsYieldedEnabled', 'TokenAllocation',
             'QuotaTokens', 'TotalWaitingTimeInMins', 'EstimatedRemainingRunningTimeInMins', 'IsQuotaFullyLoad',
             'WhetherHasSLA', 'Priority']]
        data_df['YieldScopePriority_X'] = data_df['YieldScopePriority_X'].astype(str)
        data_df['YieldScopePriority_Y'] = data_df['YieldScopePriority_Y'].astype(str)
        row = data_df.index[(data_df['YieldScopePriority_X'] != 'nan') & (data_df['YieldScopePriority_X'] != '0.0') & (
                data_df['YieldScopePriority_X'] != '1.0')]
        data_df.loc[row, 'YieldScopePriority_X'] = '2.0'
        row2 = data_df.index[(data_df['YieldScopePriority_Y'] != 'nan') & (data_df['YieldScopePriority_Y'] != '0.0') & (
                data_df['YieldScopePriority_Y'] != '1.0')]
        data_df.loc[row2, 'YieldScopePriority_Y'] = '2.0'
        data_dummy_df = pd.get_dummies(data_df)
        train_df, test_df = np.split(data_dummy_df.sample(frac=1), [int(.7 * len(data_df))])
        train_priority = train_df.pop('Priority')
        test_priority = test_df.pop('Priority')
        X_train = train_df.values
        X_test = test_df.values
        self.rf = RandomForestRegressor(n_estimators=225, max_features=0.7, random_state=15)
        self.rf.fit(X_train, train_priority)

        pre = self.rf.predict(X_test)
        print('泛化误差mse和均值(参考用):')
        print(np.sqrt(mean_squared_error(pre, test_priority)), np.mean(test_priority))

    def predict(self, job, t):
        # 这里输入的是job，应该把job的成员变量作为输入，然后输出是priority，并赋值给job
        # 要把job的格式转换一下
        isSLAJob = 1 - (job.SLA is None)
        YieldScopePriority_X_0 = 0
        YieldScopePriority_X_1 = 0
        YieldScopePriority_X_2 = 0
        YieldScopePriority_X_nan = 0
        YieldScopePriority_Y_0 = 0
        YieldScopePriority_Y_1 = 0
        YieldScopePriority_Y_2 = 0
        YieldScopePriority_Y_nan = 0
        if job.priorityX == 0.0:
            YieldScopePriority_X_0 = 1
        elif job.priorityX == 1.0:
            YieldScopePriority_X_1 = 1
        elif job.priorityX == 2.0:
            YieldScopePriority_X_2 = 1
        elif np.isnan(job.priorityX) or job.priorityX is None:
            YieldScopePriority_X_nan = 1
        else:
            YieldScopePriority_X_2 = 1

        if job.priorityY == 0.0:
            YieldScopePriority_Y_0 = 1
        elif job.priorityY == 1.0:
            YieldScopePriority_Y_1 = 1
        elif job.priorityY == 2.0:
            YieldScopePriority_Y_2 = 1
        elif np.isnan(job.priorityY) or job.priorityY is None:
            YieldScopePriority_Y_nan = 1
        else:
            YieldScopePriority_Y_2 = 1

        if job.estimated_running_time_in_min is None or np.isnan(job.estimated_running_time_in_min):
            estimated_time = 360
        else:
            estimated_time = job.estimated_running_time_in_min

        if np.isnan(job.can_yield_for):
            can_yield_for = 0
        else:
            can_yield_for = job.can_yield_for
        if np.isnan(job.can_be_yielded):
            can_be_yielded = 0
        else:
            can_be_yielded = job.can_be_yielded

        data = {'IsYieldForEnabled': can_yield_for,
                'IsYieldedEnabled': can_be_yielded,
                'TokenAllocation': [job.token],
                'QuotaTokens': [job.au.quota],
                'TotalWaitingTimeInMins': [(t - job.submit_time).total_seconds() / 60],
                'EstimatedRemainingRunningTimeInMins': [estimated_time],
                'IsQuotaFullyLoad': [job.au.is_fully],
                'WhetherHasSLA': [isSLAJob],
                'YieldScopePriority_X_0.0': [YieldScopePriority_X_0],
                'YieldScopePriority_X_1.0': [YieldScopePriority_X_1],
                'YieldScopePriority_X_2.0': [YieldScopePriority_X_2],
                'YieldScopePriority_X_nan': [YieldScopePriority_X_nan],
                'YieldScopePriority_Y_0.0': [YieldScopePriority_Y_0],
                'YieldScopePriority_Y_1.0': [YieldScopePriority_Y_1],
                'YieldScopePriority_Y_2.0': [YieldScopePriority_Y_2],
                'YieldScopePriority_Y_nan': [YieldScopePriority_Y_nan]
                }
        data_df = DataFrame(data, dtype='float32')
        X_data = data_df.values
        pre = self.rf.predict(X_data)
        job.predict_priority = round(pre[0])
        return
