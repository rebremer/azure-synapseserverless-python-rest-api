USE roboticsdemo; 
CREATE USER [test-extsynapi-app] FROM EXTERNAL PROVIDER;                       
ALTER ROLE [db_datareader] ADD MEMBER [test-extsynapi-app];
 
GRANT EXECUTE ON OBJECT::dbo.get_taxidata
    TO [test-extsynapi-app];  
GO  

GRANT EXECUTE ON OBJECT::dbo.get_taxidataAmount
    TO [test-extsynapi-app];  
GO 