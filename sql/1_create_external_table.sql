IF NOT EXISTS (SELECT * FROM sys.external_file_formats WHERE name = 'SynapseParquetFormat') 
	CREATE EXTERNAL FILE FORMAT [SynapseParquetFormat] 
	WITH ( FORMAT_TYPE = PARQUET)
GO

IF NOT EXISTS (SELECT * FROM sys.external_data_sources WHERE name = 'taxidata_testextsynapistor_dfs_core_windows_net') 
	CREATE EXTERNAL DATA SOURCE [taxidata_testextsynapistor_dfs_core_windows_net] 
	WITH (
		LOCATION   = 'https://<<your storage account attached to Synapse>>.dfs.core.windows.net/taxidata', 
	)
Go

CREATE EXTERNAL TABLE taxidemo (
	[VendorID] smallint,
	[tpep_pickup_datetime] datetime2(7),
	[tpep_dropoff_datetime] datetime2(7),
	[passenger_count] smallint,
	[trip_distance] float,
	[RatecodeID] smallint,
	[store_and_fwd_flag] bit,
	[PULocationID] smallint,
	[DOLocationID] smallint,
	[payment_type] smallint,
	[fare_amount] float,
	[extra] float,
	[mta_tax] float,
	[tip_amount] float,
	[tolls_amount] float,
	[improvement_surcharge] float,
	[total_amount] float,
	[congestion_surcharge] float
	)
	WITH (
	LOCATION = '*/*.parquet',
	DATA_SOURCE = [taxidata_testextsynapistor_dfs_core_windows_net],
	FILE_FORMAT = [SynapseParquetFormat]
	)
GO
