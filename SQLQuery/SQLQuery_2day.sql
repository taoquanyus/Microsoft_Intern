/****** select two days data as test sets in mock_cosmos to compare ML-based and Quota-management scheduler indicator ******/
WITH hisinfo
AS(
SELECT [JobId]
	  ,[AUId]
      ,[JobRegistryId]
      ,[SLA]
      ,[Allocation] as jobToken
      ,[SubmitTime]
      ,[TotalRunningTimeInMinutes]
  FROM [JobScheduling].[dbo].[HistoricalJobInfo]
  where SubmitTime>'2021-09-13' and SubmitTime<'2021-09-15' and VCId=100 and JobStateId=2
  -- order by SubmitTime desc
),

cte2
AS(
select [JobId]
	  ,[hisinfo].AUId
      ,[SLA]
      ,jobToken
      ,[SubmitTime]
      ,[TotalRunningTimeInMinutes]
	  ,[YieldScopePriority_X] as priorityX
	  ,[YieldScopePriority_Y] as priorityY
	  ,[IsYieldForEnabled]
	  ,[IsYieldedEnabled]
	  ,[EstimatedRunningTimeInMins]
	  from hisinfo inner join v_JobRegistrationVNextAll on hisinfo.JobRegistryId=v_JobRegistrationVNextAll.JobRegistryId
)

select * from cte2 order by SubmitTime 



/*
cte3
AS(
select cte2.[JobId]
	  ,cte2.AUId
      ,cte2.[JobRegistryId]
      ,cte2.[SLA]
      ,jobToken
      ,[SubmitTime]
      ,[TotalWaitingTimeInMinutes]
      ,[TotalRunningTimeInMinutes]
	  ,priorityX
	  ,priorityY
	  ,cte2.[IsYieldForEnabled]
	  ,cte2.[IsYieldedEnabled]
	  ,[EstimatedRunningTimeInMins]
	  from cte2 inner join JobSchedulingRecord on cte2.JobId=JobSchedulingRecord.JobId
)
select * from cte3
*/