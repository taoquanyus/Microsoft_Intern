# 读python file
# 读python
import numpy as np
import pandas as pd

all_df = pd.read_csv('./data_v1.csv', index_col=0)
# all_df = all_df.sample(frac=1)
# all_df = all_df.reset_index(drop=True)
# all_df['IsQuotaFullyLoad'] = np.random.randint(0, 2, size=len(all_df))
# all_df['Priority'] = 9999
# all_df['WhetherHasSLA'] = 0
# all_df['WhetherHasSLA'] = ~pd.isnull(all_df['SLA'])
# all_df['WhetherHasSLA'] = all_df['WhetherHasSLA'] + 0
all_df = all_df[
    ['YieldScopePriority_X', 'YieldScopePriority_Y', 'IsYieldForEnabled', 'IsYieldedEnabled', 'TokenAllocation',
     'QuotaTokens', 'TotalWaitingTimeInMins', 'EstimatedRemainingRunningTimeInMins', 'IsQuotaFullyLoad',
     'WhetherHasSLA', 'Priority']]

all_df['Priority'] = 0
for index, row in all_df.iterrows():
    value_YieldScopePriority_X = 0
    if row['YieldScopePriority_X'] == 0:
        value_YieldScopePriority_X = 20
    elif row['YieldScopePriority_X'] == 1:
        if row['YieldScopePriority_Y'] == 0:
            value_YieldScopePriority_X = 50
        else:
            value_YieldScopePriority_X = 60
    elif row['YieldScopePriority_X'] == 2:
        value_YieldScopePriority_X = 80
    else:
        value_YieldScopePriority_X = 90
    row['Priority'] += value_YieldScopePriority_X

    value_Yield_Enable = 0
    if row['IsYieldForEnabled'] == 0:
        value_Yield_Enable += 5
    if row['IsYieldedEnabled'] == 0:
        value_Yield_Enable += 8
    row['Priority'] += value_Yield_Enable

    value_token_quota_ratio = 0
    quota_indicator = row['QuotaTokens'] / row['TokenAllocation']
    if quota_indicator < 1:
        value_token_quota_ratio = 10
    elif 1 <= quota_indicator < 5:
        value_token_quota_ratio = 5
    elif 5 <= quota_indicator < 8:
        value_token_quota_ratio = 3
    elif 8 <= quota_indicator < 15:
        value_token_quota_ratio = -5
    elif quota_indicator:
        value_token_quota_ratio = -10
    row['Priority'] += value_token_quota_ratio

    value_time_waiting = 0
    if row['TotalWaitingTimeInMins'] <= 300:
        value_time_waiting = round(row['TotalWaitingTimeInMins'] / 15)
    elif 300 < row['TotalWaitingTimeInMins'] <= 600:
        value_time_waiting = round(row['TotalWaitingTimeInMins'] / 25)
    else:
        value_time_waiting = round(row['TotalWaitingTimeInMins'] / 100)

    row['Priority'] += value_time_waiting

    value_estimated_time = 0
    if row['EstimatedRemainingRunningTimeInMins'] == 5:
        value_estimated_time = 0
    elif row['EstimatedRemainingRunningTimeInMins'] == 7:
        value_estimated_time = 2
    elif row['EstimatedRemainingRunningTimeInMins'] == 30:
        value_estimated_time = 5
    elif row['EstimatedRemainingRunningTimeInMins'] == 40:
        value_estimated_time = 8
    elif row['EstimatedRemainingRunningTimeInMins'] == 45:
        value_estimated_time = 9
    elif row['EstimatedRemainingRunningTimeInMins'] == 50:
        value_estimated_time = 10
    elif row['EstimatedRemainingRunningTimeInMins'] == 60:
        value_estimated_time = 12
    elif row['EstimatedRemainingRunningTimeInMins'] == 120:
        value_estimated_time = 20
    elif row['EstimatedRemainingRunningTimeInMins'] == 180:
        value_estimated_time = 25
    elif row['EstimatedRemainingRunningTimeInMins'] == 360:
        value_estimated_time = 50
    else:
        value_estimated_time = 51

    row['Priority'] += value_estimated_time

    value_quota_fully_load = 0
    if row['IsQuotaFullyLoad'] == 1:
        value_quota_fully_load = 20
    row['Priority'] += value_quota_fully_load

    value_SLA = 0
    if row['WhetherHasSLA'] == 0:
        value_SLA = 20
    row['Priority'] += value_SLA

    rdm = np.random.randint(0, 3)
    row['Priority'] += rdm

    all_df.iloc[index] = row

all_df['Priority'] -= 40
all_df.to_csv(path_or_buf='./data_v1.csv')
