import numpy as np
import pandas as pd
import pprint
import random

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 5000)
np.set_printoptions(linewidth=300)

data_all_df = pd.read_csv('./inputs/raw_data/all_table_3000_2.csv', index_col=0)
data_sla_df = pd.read_csv('./inputs/raw_data/sla_not_null_500_2.csv', index_col=0)
data_prixy_df = pd.read_csv('./inputs/raw_data/priorityxy_not_null_500_2.csv', index_col=0)
all_df = pd.concat((data_all_df, data_sla_df, data_prixy_df), axis=0)
all_df = all_df.reset_index(drop=True)
# 判断是否存在SLA
all_df['isExceedSLA'] = 0
all_df['isExceedSLA'] = ~pd.isnull(all_df['SLA'])
all_df.head()

all_df = all_df.drop(['JobId', 'Priority', 'AUId', 'VCId', 'random', 'JobRegistryId', 'SLA', 'JobStateId'], axis=1)
print(all_df.head())
all_df.describe()
# 添加一列AU是否满载，用0,1随机数来填充
all_df['IsQuotaFullyLoad'] = np.random.randint(0, 2, size=len(all_df))
# 乱序
all_df = all_df.sample(frac=1)
all_df = all_df.reset_index(drop=True)
all_df['Priority'] = 9999
all_df = all_df[
    ['YieldScopePriority_X', 'YieldScopePriority_Y', 'IsYieldForEnabled', 'IsYieldedEnabled', 'TokenAllocation',
     'QuotaTokens', 'TotalWaitingTimeInMins', 'IsQuotaFullyLoad', 'isExceedSLA', 'Priority']]

[rows, columns] = [all_df.shape[0], all_df.shape[1]]
print([rows, columns])
for index in range(rows):
    if index < 50:
        # 打印未排序的全部jobs
        control_group = all_df.iloc[0:index]
    else:
        # 仅打印排序的20个jobs
        collection = range(index)
        nums = random.sample(collection, 20)
        control_group = all_df.iloc[nums]

    control_group = control_group.sort_values(by="Priority", ascending=True)

    control_group = control_group.append(all_df.iloc[index])

    pprint.pprint(control_group)
    str_input = "job " + str(index) + "\'s priority："
    temp = input(str_input)
    if temp == "modify":
        modify_index = input('what index you wanna modify?')
        modify_priority = input('please input updated priority.')
        all_df.loc[modify_index, 'Priority'] = int(modify_priority)
        index = index-1
    else:
        all_df.loc[index, 'Priority'] = int(temp)

    if index % 50 == 0:
        all_df.to_csv(path_or_buf='./labelled_data.csv')
# 保存dataframe
all_df.to_csv(path_or_buf='./labelled_data.csv')
