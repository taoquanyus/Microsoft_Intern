# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import copy
import functools
import AU
import Compare
import VC
import Job
import matplotlib.pyplot as plt
from MLModel import MlModel

import datetime
import time
import pandas as pd

current_time = datetime.datetime(2021, 9, 1)
# 几个变量
'''
jobs_list       全部的jobs
ranked_list     submit_time<current_time && remaining_time<=0
running_list    正在run的jobs
waiting_list    已经提交但是没有run的jobs
'''


def main():
    aus = pd.read_csv("./input/AU_Hierarchy.csv")
    jobs = pd.read_csv("./input/Jobs_OrderBySubmitTime.csv")
    au_list = build_au_tree(aus)  # 完成建立AU tree
    jobs_list = build_jobs_list(jobs)  # 完成建立jobs的list
    # 把dataframe中的job一个个生成job类，存到list中

    # 使用当前的Quota management进行schedule
    ares_scheduler_run(jobs_list)

    # 使用ML进行schedule
    machine_learning_run(jobs_list)


# 建立一个AU树，把每个AU的子AU都找到，然后按照hierarchy来排序
def build_au_tree(aus):
    aus_list = []
    au_dict = {}
    for index, row in aus.iterrows():
        print(row['AUID'])
        au_id = row['AUID']
        token = row['QuotaTokens']
        parent_au = row['ParentID']
        au_hierarchy = row['HierarchyLevel']
        temp_au = AU.AU(au_id, token, parent_au, au_hierarchy)
        au_dict[au_id] = temp_au
        aus_list.append(temp_au)

    # 所有的AU找到其父节点
    for father in aus_list:
        for each_au in aus_list:
            if each_au.parent_au_id == father.au_id:
                father.add_child(each_au)

    aus_list.sort(key=AU.AU.get_hierarchy)

    return aus_list


# 建立一个job的列表，并按照提交时间顺序排序
def build_jobs_list(jobs):
    jobs_list = []
    for index, row in jobs.iterrows():
        print(row['JobId'])
        job_id = row['JobId']
        token = row['jobToken']
        priority_x = row['priorityX']
        priority_y = row['priorityY']
        au_id = row['AUId']
        submit_time = row['SubmitTime']
        can_be_yielded = row['IsYieldedEnabled']
        can_yield_for = row['IsYieldForEnabled']
        running_time = row['TotalRunningTimeInMinutes']
        estimated_time = row['EstimatedRunningTimeInMins']
        SLA = row['SLA']
        temp = Job.Job(job_id, au_id, token, SLA, priority_x, priority_y, submit_time, can_be_yielded,
                       can_yield_for, running_time, estimated_time)
        temp.au = AU.AU.maps.get(au_id)
        jobs_list.append(temp)

    jobs_list.sort(key=Job.Job.get_submit_time)
    return jobs_list


# quota management 的比较方法


def ares_scheduler_run(jobs_list):
    # VC 的一些属性的设置
    waiting_jobs = copy.deepcopy(jobs_list)  # 所有job的list,并按照submit time排序
    vc = VC.VC(snap_interval=datetime.timedelta(minutes=1), call_interval=datetime.timedelta(minutes=6),
               sum_token=136258)

    # vc.snap_interval = datetime.time(0, 1, 0, 0)  #cosmos 刷新的时间,1min一次
    # vc.call_interval = datetime.time(0, 6, 0, 0)  #scheduler call的时间 6分钟一次

    start_time = copy.deepcopy(waiting_jobs[0].submit_time)
    # start_time = start_time.split('.')
    # start_time = start_time[0]
    # start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    # end_time = copy.deepcopy(waiting_jobs[-1].submit_time)
    t = start_time

    finish_list = []  # 已经完成job的list
    join_list = []  # 在当前时间点已经提交的job的list
    call_interval = vc.call_interval - vc.snap_interval
    vc_load = []
    while len(finish_list) != len(jobs_list):  # job 还没有跑完

        t += vc.snap_interval
        call_interval += vc.snap_interval
        for temp_job in waiting_jobs:
            if t > temp_job.submit_time:  # 先把有效的job添加进来
                join_list.append(temp_job)
                waiting_jobs.remove(temp_job)
        # todo:
        #  update jobs information
        #   策略，不更新job的等待时间，等待时间最后拿finish_time-submit_time-running_time计算
        #   更新VC的信息(spare_token)
        for temp_job in vc.running_jobs:
            temp_job.remaining_time -= vc.snap_interval

        #  remove job from cosmos if it has been finished
        for temp_job in vc.running_jobs:
            if temp_job.remaining_time <= datetime.timedelta(0):
                temp_job.finish_time = t  # finish_time
                vc.finish_running_jobs(temp_job)
                finish_list.append(temp_job)
                join_list.remove(temp_job)

        # cosmos call
        # 应该是所有的job重新排版一遍，然后添加进去新的job，暂停的job status设置为0
        yield_limit = vc.yield_limit
        if call_interval >= vc.call_interval:  # 每6分钟调用一次
            call_interval = datetime.timedelta(0)
            if len(join_list) == 0:
                continue
            join_list.sort(key=functools.cmp_to_key(Compare.compare_quota))  # sorts

            # 有空位就先把job添加进去
            for temp_job in join_list:
                if vc.running_jobs.__contains__(temp_job):
                    continue
                if vc.spare_token >= temp_job.token:
                    vc.add_running_jobs(temp_job)

            # yield掉一些jobs
            for temp_job in join_list:
                #  job
                yield_limit -= 1
                if yield_limit == 0:
                    break
                if temp_job.can_yield_for == 1 and temp_job.status == 0:
                    for run_job in vc.running_jobs:
                        if Compare.compare_quota(temp_job,
                                                 run_job) == -1 and temp_job.token < run_job.token + vc.spare_token:
                            vc.remove_running_jobs(run_job)
                            vc.add_running_jobs(temp_job)
        vc_load.append(vc.running_token)

    # todo:data visualization
    plt.plot(vc_load)
    plt.show()
    # 还有sla的格式和其他数据格式的错误还没有修改
    # 1.jobs的延迟时间
    # 把每个job取出，用dataframe排好并输出
    data = []
    for each_job in finish_list:
        data.append([each_job.job_id, each_job.au_id, each_job.SLA, each_job.token, each_job.submit_time
                        , each_job.total_time, each_job.priorityX, each_job.priorityY, each_job.can_yield_for,
                     each_job.can_be_yielded, each_job.estimated_running_time, each_job.latency_time])
    df = pd.DataFrame(data, columns=['JobId', 'AUId', 'SLA', 'jobToken', 'SubmitTime', 'TotalRunningTime', 'priorityX',
                                     'priorityY', 'isYieldForEnable', 'isYieldedEnable', 'EstimatedRunningTimeInMins',
                                     'LatencyTime'])

    df.to_csv("./output/jobs_output.csv")


def machine_learning_run(jobs_list):
    # 1.和上文的方法不同只是排序的手段不同
    # 2.一样的用法，需要yield，需要，最后算集群的使用率

    waiting_jobs = copy.deepcopy(jobs_list)  # 所有job的list,并按照submit time排序

    vc = VC.VC(snap_interval=datetime.timedelta(minutes=1), call_interval=datetime.timedelta(minutes=6),
               sum_token=136258)
    start_time = copy.deepcopy(waiting_jobs[0].submit_time)
    t = start_time
    finish_list = []  # 已经完成job的list
    join_list = []  # 在当前时间点已经提交的job的list
    call_interval = vc.call_interval - vc.snap_interval
    vc_load = []

    model = MlModel()
    model.train()

    while len(finish_list) != len(jobs_list):  # job 还没有跑完

        t += vc.snap_interval
        call_interval += vc.snap_interval
        for temp_job in waiting_jobs:
            if t > temp_job.submit_time:  # 先把有效的job添加进来
                join_list.append(temp_job)
                waiting_jobs.remove(temp_job)
        # todo:
        #  update jobs information
        #   策略，不更新job的等待时间，等待时间最后拿finish_time-submit_time-running_time计算
        #   更新VC的信息(spare_token)
        for temp_job in vc.running_jobs:
            temp_job.remaining_time -= vc.snap_interval

        #  remove job from cosmos if it has been finished
        for temp_job in vc.running_jobs:
            if temp_job.remaining_time <= datetime.timedelta(0):
                temp_job.finish_time = t  # finish_time
                vc.finish_running_jobs(temp_job)
                finish_list.append(temp_job)
                join_list.remove(temp_job)

        # cosmos call
        # 应该是所有的job重新排版一遍，然后添加进去新的job，暂停的job status设置为0
        yield_limit = vc.yield_limit
        if call_interval >= vc.call_interval:  # 每6分钟调用一次,每次调用都要重新赋值一遍，因为不同的job的等待时间会发生变化
            for each_job in join_list:
                # 直接给job的priority赋值
                # print(each_job.job_id)
                model.predict(each_job, t)
            call_interval = datetime.timedelta(0)  # 归零
            if len(join_list) == 0:
                continue
            join_list.sort(key=functools.cmp_to_key(Compare.compare_ML))  # sorts

            # 有空位就先把job添加进去
            for temp_job in join_list:
                if vc.running_jobs.__contains__(temp_job):
                    continue
                if vc.spare_token >= temp_job.token:
                    vc.add_running_jobs(temp_job)

            # yield掉一些jobs
            for temp_job in join_list:
                #  job
                yield_limit -= 1
                if yield_limit == 0:
                    break
                if temp_job.can_yield_for == 1 and temp_job.status == 0:
                    for run_job in vc.running_jobs:
                        if Compare.compare_ML(temp_job,
                                              run_job) < 0 and temp_job.token < run_job.token + vc.spare_token:
                            vc.remove_running_jobs(run_job)
                            vc.add_running_jobs(temp_job)
        vc_load.append(vc.running_token)
        # if len(finish_list) == 1191:
        #     temp=1
        print('have finished:', len(finish_list), '/', len(jobs_list))
        time.sleep(0.01)

    plt.plot(vc_load)
    plt.show()
    # 还有sla的格式和其他数据格式的错误还没有修改
    # 1.jobs的延迟时间
    # 把每个job取出，用dataframe排好并输出
    data = []
    for each_job in finish_list:
        data.append([each_job.job_id, each_job.au_id, each_job.SLA, each_job.token, each_job.submit_time
                        , each_job.total_time, each_job.priorityX, each_job.priorityY, each_job.can_yield_for,
                     each_job.can_be_yielded, each_job.estimated_running_time, each_job.latency_time])
    df = pd.DataFrame(data,
                      columns=['JobId', 'AUId', 'SLA', 'jobToken', 'SubmitTime', 'TotalRunningTime', 'priorityX',
                               'priorityY', 'isYieldForEnable', 'isYieldedEnable', 'EstimatedRunningTimeInMins',
                               'LatencyTime'])

    df.to_csv("./output/jobs_output_ml.csv")


if __name__ == '__main__':
    main()
