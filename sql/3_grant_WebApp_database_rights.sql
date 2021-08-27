CREATE USER [<<web app name>>] FROM EXTERNAL PROVIDER;                       
ALTER ROLE [db_datareader] ADD MEMBER [<<web app name>>];
 
GRANT EXECUTE ON OBJECT::dbo.get_taxidata
    TO [<<web app name>>];  
GO  

GRANT EXECUTE ON OBJECT::dbo.get_taxidataAmount
    TO [<<web app name>>];  
GO 