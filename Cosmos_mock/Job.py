import copy
import datetime
import time


def T(submit_time):
    submit_time = submit_time.split('.')[0]
    submit_time = datetime.datetime.strptime(submit_time, '%Y-%m-%d %H:%M:%S')
    return submit_time


def T_inMin(timeInMins):
    if timeInMins != timeInMins:  # python Nan的一个性质就是自己与自己不相等
        return datetime.timedelta(0)
    return datetime.timedelta(minutes=timeInMins)


class Job:

    def __init__(self, job_id, au_id, token, SLA, priority_x, priority_y, submit_time, can_be_yielded,
                 can_yield_for, running_time, estimated_running_time):
        self.latency_time = datetime.time(0, 0, 0, 0)
        self.job_id = job_id
        self.token = token
        self.priorityX = priority_x
        self.priorityY = priority_y
        self.SLA = SLA
        self.status = 0
        self.last_priority = 2000
        self.predict_priority = 2000
        self.au_id = au_id
        self.submit_time = T(submit_time)
        self.can_be_yielded = can_be_yielded
        self.can_yield_for = can_yield_for
        self.total_time = 0
        self.running_time = T_inMin(running_time)
        self.remaining_time = copy.deepcopy(self.running_time)
        self.finish_time = datetime.datetime(1,1,1,0,0)
        self.estimated_running_time_in_min = estimated_running_time
        self.estimated_running_time = T_inMin(self.estimated_running_time_in_min)
        self.au = None

    def get_submit_time(self):
        return self.submit_time

    def set_running(self):
        self.status = 1
        self.au.quota -= self.token
        if self.au.quota < 0:
            self.au.is_fully = 1
        else:
            self.au.is_fully = 0

    def set_pausing(self):
        self.status = 0
        self.au.quota += self.token
        if self.au.quota < 0:
            self.au.is_fully = 1
        else:
            self.au.is_fully = 0

    def set_finished(self):
        self.status = 2
        self.au.quota += self.token
        if self.au.quota < 0:
            self.au.is_fully = 1
        else:
            self.au.is_fully = 0
        self.latency_time = self.finish_time - self.submit_time - self.running_time
