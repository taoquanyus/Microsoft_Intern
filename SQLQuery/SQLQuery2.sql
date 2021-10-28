SELECT TOP (10000) [JobId]
      ,[JobRegistryId]
      ,[JobNamingId]
      ,[JobName]
      ,[JobDate]
      ,[SLA]
      ,[JobStateId]
      ,[Allocation]
      ,[SubmitTime]
      ,[SubmitDatePst]
      ,[AUId]
	  ,[JobScheduling].[dbo].[AllocationUnitHierarchy].[Name] AS [AUName]
	  ,T3.[totalTokens]
      ,[JobCategory]
	  ,[JobPriority]
  FROM 
  ([JobScheduling].[dbo].[HistoricalJobInfo] INNER JOIN [JobScheduling].[dbo].[AllocationUnitHierarchy] ON [JobScheduling].[dbo].[HistoricalJobInfo].AUid=[JobScheduling].[dbo].[AllocationUnitHierarchy].ID)
  
  LEFT JOIN(SELECT [TimeStamp],[JobScheduling].[dbo].[v_Reporting_AURealtimeStatus].[AUName],([Tokens]+[RunningTokens]+[WaitingTokens]) AS totalTokens FROM [JobScheduling].[dbo].[v_Reporting_AURealtimeStatus] 
		INNER JOIN (SELECT [AUName],max([TimeStamp]) AS LatestTime FROM [JobScheduling].[dbo].[v_Reporting_AURealtimeStatus] WHERE TimeStamp<'2021-07-25' group by(AUName)) AS T2 ON [JobScheduling].[dbo].[v_Reporting_AURealtimeStatus].[AUName]=T2.[AUName] AND [TimeStamp]=T2.LatestTime)AS T3
  ON [AUName]=T3.AUName

  

  WHERE JobRegistryId IS NOT NULL AND AUId IS NOT NULL AND LastUpdateTime>'2021-07-25'