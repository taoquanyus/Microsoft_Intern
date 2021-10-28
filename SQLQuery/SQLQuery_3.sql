WITH cte1
AS (
　　SELECT TOP(1000) [TimeStamp]
	  ,[JobId]
      ,[JobStateId]
      ,[Priority]
      ,[TokenAllocation]
	  ,[QuotaTokens]
	  ,[AUId]
	  ,t1.[VCId]
	  ,[TotalWaitingTimeInMins]
	  ,newid() random
　　FROM [JobScheduling].[dbo].[JobSnapshot] as t1 inner join [JobScheduling].[dbo].[AllocationUnitHierarchy] as t2 on t1.[AUId]=t2.[ID]
　　WHERE t1.Priority>80 AND t1.Priority<3000 AND t1.VCId=100 order by random
),
--cte1 和 [HistoricalJobInfo]

cte2
AS(
	select TOP(1000) [TimeStamp]
	  ,cte1.[JobId]
      ,cte1.[JobStateId]
      ,[Priority]
      ,[TokenAllocation]
	  ,[QuotaTokens]
	  ,cte1.[AUId]
	  ,cte1.[VCId]
	  ,[TotalWaitingTimeInMins]
	  ,[random]
	  ,[SLA]
	  ,[JobRegistryId]
	  From cte1 inner join [HistoricalJobInfo] as t3 on cte1.[JobId]=t3.[JobId]
	  order by random
)

--select top(1000) 
--*
--from cte2

select top(1000) [TimeStamp]
	,cte2.[JobId]
    ,cte2.[JobStateId]
    ,[Priority]
    ,[TokenAllocation]
	,[QuotaTokens]
    ,cte2.[AUId]
	,cte2.[VCId]
	,[TotalWaitingTimeInMins]
	,[random]
	,[SLA]
	,cte2.[JobRegistryId]
    ,t4.IsYieldedEnabled
	,t4.IsYieldForEnabled
	,YieldScopePriority_X
	,YieldScopePriority_Y
	from [cte2] inner join v_JobRegistrationVNextAll as t4 on cte2.JobRegistryId=t4.[JobRegistryId]