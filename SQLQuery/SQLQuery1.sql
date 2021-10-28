/****** Script for SelectTopNRows command from SSMS  ******/
/*SELECT [TimeStamp]
	  ,[JobScheduling].[dbo].[v_Reporting_AURealtimeStatus].[AUName]
      ,[Cluster]
      ,[VCName]
      ,[Tokens]
      ,[RunningJobs]
      ,[WaitingJobs]
      ,[RunningTokens]
      ,[WaitingTokens]
      ,[YieldedJobsTotal]
      ,[YieldedJobsLatestInterval]
      ,[YieldedTokensLatestInterval]
	  ,([Tokens]+[RunningTokens]+[WaitingTokens]) AS totalTokens
  FROM [JobScheduling].[dbo].[v_Reporting_AURealtimeStatus]
  INNER JOIN (SELECT [AUName],
	max([TimeStamp]) AS LatestTime
  FROM [JobScheduling].[dbo].[v_Reporting_AURealtimeStatus]
  WHERE TimeStamp<'2021-07-25'
  group by(AUName)) AS T2
  ON [JobScheduling].[dbo].[v_Reporting_AURealtimeStatus].[AUName]=T2.[AUName] AND [TimeStamp]=T2.LatestTime
  */

--SELECT [TimeStamp],[JobScheduling].[dbo].[v_Reporting_AURealtimeStatus].[AUName],([Tokens]+[RunningTokens]+[WaitingTokens]) AS totalTokens FROM [JobScheduling].[dbo].[v_Reporting_AURealtimeStatus] 
--INNER JOIN (SELECT [AUName],max([TimeStamp]) AS LatestTime FROM [JobScheduling].[dbo].[v_Reporting_AURealtimeStatus] WHERE TimeStamp<'2021-07-25' group by(AUName)) AS T2 ON [JobScheduling].[dbo].[v_Reporting_AURealtimeStatus].[AUName]=T2.[AUName] AND [TimeStamp]=T2.LatestTime

--SELECT TOP (1000) [JobId]
--      ,[JobRegistryId]
--      ,[JobNamingId]
--      ,[JobName]
--      ,[JobDate]
--      ,[SLA]
--      ,[JobStateId]
--      ,[Allocation]
--      ,[SubmitTime]
--      ,[SubmitDatePst]
--      ,[AUId]
--	  ,[JobScheduling].[dbo].[AllocationUnitHierarchy].[Name] AS [AUName]
--      ,[JobCategory]
--	  ,[JobPriority]
--  FROM 
--  ([JobScheduling].[dbo].[HistoricalJobInfo] INNER JOIN [JobScheduling].[dbo].[AllocationUnitHierarchy] ON [JobScheduling].[dbo].[HistoricalJobInfo].AUid=[JobScheduling].[dbo].[AllocationUnitHierarchy].ID)
--  order by LastUpdateTime

  --SELECT TOP (1000) [JobId]
  --    ,[JobRegistryId]
  --    ,[JobNamingId]
  --    ,[JobName]
  --    ,[JobDate]
  --    ,[SLA]
  --    ,[JobStateId]
  --    ,[Allocation]
  --    ,[SubmitTime]
  --    ,[SubmitDatePst]
  --    ,[AUId]
	 -- ,[JobScheduling].[dbo].[AllocationUnitHierarchy].[Name] AS [AUName]
	 -- ,T3.[totalTokens]
  --    ,[JobCategory]
	 -- ,[JobPriority]
  --FROM 
  --([JobScheduling].[dbo].[HistoricalJobInfo] INNER JOIN [JobScheduling].[dbo].[AllocationUnitHierarchy] ON [JobScheduling].[dbo].[HistoricalJobInfo].AUid=[JobScheduling].[dbo].[AllocationUnitHierarchy].ID)--前两个表
  --INNER JOIN(SELECT [TimeStamp],[JobScheduling].[dbo].[v_Reporting_AURealtimeStatus].[AUName],([Tokens]+[RunningTokens]+[WaitingTokens]) AS totalTokens FROM [JobScheduling].[dbo].[v_Reporting_AURealtimeStatus] 
		--INNER JOIN (SELECT [AUName],max([TimeStamp]) AS LatestTime FROM [JobScheduling].[dbo].[v_Reporting_AURealtimeStatus] WHERE TimeStamp<'2021-07-25' group by(AUName)) AS T2 ON [JobScheduling].[dbo].[v_Reporting_AURealtimeStatus].[AUName]=T2.[AUName] AND [TimeStamp]=T2.LatestTime)AS T3
  --ON [JobScheduling].[dbo].[AllocationUnitHierarchy].[Name]=T3.AUName
  --WHERE JobRegistryId IS NOT NULL AND AUId IS NOT NULL AND LastUpdateTime>'2021-07-25'

-- 数据库数据读表
SELECT TOP(2000) [JobId]
,[JobDate]
,[HistoricalJobInfo].[VCId]
,[SLA]
,[JobStateId]
,[Allocation]
,[SubmitTime]
,[HistoricalJobInfo].[AUid]
,[QuotaTokens]
,[JobPriority]
,[YieldScopePriority_X]
,[YieldScopePriority_Y]
,NEWID() AS random

FROM HistoricalJobInfo inner join AllocationUnitHierarchy on [HistoricalJobInfo].AUId=AllocationUnitHierarchy.ID
inner join [v_JobRegistrationVNextAll] ON HistoricalJobInfo.JobRegistryId=[v_JobRegistrationVNextAll].JobRegistryId
where [HistoricalJobInfo].VCId=100 and YieldScopePriority_X is not null and YieldScopePriority_Y is not null
order by random