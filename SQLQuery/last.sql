/****** Script for SelectTopNRows command from SSMS  ******/
with cte1
AS(
SELECT TOP (500) [TimeStamp]
      ,[JobId]
      ,[SchedulingIntervalInSecs]
      ,[AUId]
      ,[JobStateId]
      ,[Priority]
      ,[TokenAllocation]
      ,[TotalWaitingTimeInMins]
      ,[TotalYieldTimeInMins]
      ,[TotalRunningTimeInMins]
      ,[EstimatedRemainingRunningTimeInMins]
      ,[VertexProgress]
	  ,AllocationUnitHierarchy.QuotaTokens
	  ,newid() random 
  FROM [JobScheduling].[dbo].[JobSnapshot]
  inner join AllocationUnitHierarchy on JobSnapshot.AUId=AllocationUnitHierarchy.ID
  where Priority>80 and Priority<2000 and JobSnapshot.VCId = 100 and TimeStamp>'2021-07-01' and TimeStamp<'2021-10-09'
  order by random
),

cte2
AS(
select TOP (500) [TimeStamp]
      ,cte1.[JobId]
      ,[SchedulingIntervalInSecs]
      ,cte1.[AUId]
      ,cte1.[JobStateId]
      ,[Priority]
      ,[TokenAllocation]
      ,[TotalWaitingTimeInMins]
      ,[EstimatedRemainingRunningTimeInMins]
	  ,QuotaTokens
	  ,HistoricalJobInfo.SLA
	  ,HistoricalJobInfo.JobRegistryId
	  from cte1 inner join HistoricalJobInfo on cte1.JobId=HistoricalJobInfo.JobId
)

select TOP (500)[JobId]
      ,[TokenAllocation]
      ,[TotalWaitingTimeInMins]
      ,[EstimatedRemainingRunningTimeInMins]
	  ,QuotaTokens
	  ,cte2.SLA
	  ,v_JobRegistrationVNextAll.YieldScopePriority_X
	  ,v_JobRegistrationVNextAll.YieldScopePriority_Y
	  ,v_JobRegistrationVNextAll.IsYieldedEnabled
	  ,v_JobRegistrationVNextAll.IsYieldForEnabled
	  from cte2 inner join v_JobRegistrationVNextAll on cte2.JobRegistryId=v_JobRegistrationVNextAll.JobRegistryId