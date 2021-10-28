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


all_df = pd.read_csv('./labelled_data.csv', index_col=0)

[rows, columns] = [all_df.shape[0], all_df.shape[1]]
index = 900
while index < rows:
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
    index = index + 1
    # 保存dataframe
all_df.to_csv(path_or_buf='./labelled_data.csv')