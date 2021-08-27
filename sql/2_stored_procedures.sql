/****** Object:  StoredProcedure [dbo].[get_taxidata]    Script Date: 8/27/2021 9:28:46 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE   PROCEDURE [dbo].[get_taxidata]
AS
SET NOCOUNT ON;
-- Cast is needed to corretly inform pyodbc of output type is NVARCHAR(MAX)
-- Needed if generated json is bigger then 4000 bytes and thus pyodbc trucates it
-- https://stackoverflow.com/questions/49469301/pyodbc-truncates-the-response-of-a-sql-server-for-json-query
	SELECT 
        top 1000 *
	FROM 
		[dbo].[taxidemo] 
	FOR JSON PATH
GO

/****** Object:  StoredProcedure [dbo].[get_taxidataAmount]    Script Date: 8/27/2021 9:29:04 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[get_taxidataAmount]
@Json NVARCHAR(MAX)
AS
SET NOCOUNT ON;
DECLARE @total_amount FLOAT = JSON_VALUE(@Json, '$.total_amount');
SET NOCOUNT ON;
-- Cast is needed to corretly inform pyodbc of output type is NVARCHAR(MAX)
-- Needed if generated json is bigger then 4000 bytes and thus pyodbc trucates it
-- https://stackoverflow.com/questions/49469301/pyodbc-truncates-the-response-of-a-sql-server-for-json-query
	SELECT 
        top 1000 *
	FROM 
		[dbo].[taxidemo] 

WHERE 
	[total_amount] = @total_amount

	FOR JSON PATH
GO


