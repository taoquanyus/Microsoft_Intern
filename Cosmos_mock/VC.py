import datetime
import functools

import Compare
import Job


class VC:
    def __init__(self, snap_interval, call_interval, sum_token):
        self.running_token = 0
        self.sum_token = sum_token
        self.running_jobs = []
        # self.queuing_jobs = []
        self.spare_token = self.sum_token - self.running_token
        self.snap_interval = snap_interval  # cosmos 刷新的时间,1min一次
        self.call_interval = call_interval  # scheduler call的时间 6分钟一次
        self.yield_limit = 15
        # self.schedule_jobs_per_round = 30

    def add_running_jobs(self, job):
        self.running_jobs.append(job)
        self.running_token += job.token
        self.spare_token = self.sum_token - self.running_token
        job.set_running()
        self.running_jobs.sort(key=functools.cmp_to_key(Compare.compare_quota), reverse=True)

    def remove_running_jobs(self, job):
        self.running_jobs.remove(job)
        self.running_token -= job.token
        self.spare_token = self.sum_token - self.running_token
        job.set_pausing()

    def finish_running_jobs(self, job):
        self.running_jobs.remove(job)
        self.running_token -= job.token
        self.spare_token = self.sum_token - self.running_token
        job.set_finished()
