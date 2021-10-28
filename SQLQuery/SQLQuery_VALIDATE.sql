/****** Script for SelectTopNRows command from SSMS  ******/
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
　　FROM [JobScheduling].[dbo].[JobSnapshot] as t1 inner join [JobScheduling].[dbo].[AllocationUnitHierarchy] as t2 on t1.[AUId]=t2.[ID]
　　WHERE TimeStamp = '2021-09-06 08:25:43.297' AND t1.Priority<81 AND t1.VCId=100
	ORDER BY [JobStateId]
	--order by [TimeStamp] desc
),

cte2
AS(
SELECT AUId, sum(tokenAllocation) as SumToken, AVG(QuotaTokens) as quota from cte1 
group by AUId
),

cte3
AS(
SELECT TimeStamp,Jobid,JobStateId,Priority,TokenAllocation,SumToken,QuotaTokens,(sign(SumToken-QuotaTokens)+1)/2 as isOverLoaded,cte1.AUId,VCId,TotalWaitingTimeInMins from cte1 inner join cte2 on cte1.AUId=cte2.AUId
  where TimeStamp = '2021-09-06 08:25:43.297'
),

cte4
AS
(
SELECT TimeStamp,JobRegistryId, cte3.JobId, cte3.JobStateId, Priority,SLA, TokenAllocation,SumToken, QuotaTokens,isOverLoaded, cte3.AUId, cte3.VCId,TotalWaitingTimeInMins from cte3 inner join HistoricalJobInfo on  cte3.JobId=HistoricalJobInfo.JobId
)


select TimeStamp,[YieldScopePriority_X],[YieldScopePriority_Y],SLA,cte4.JobStateId, Priority, TokenAllocation,SumToken, QuotaTokens,isOverLoaded, TotalWaitingTimeInMins,IsYieldForEnabled,IsYieldedEnabled from cte4 inner join v_JobRegistrationVNextAll on cte4.JobRegistryId=v_JobRegistrationVNextAll.JobRegistryId
order by JobStateId,priority
