CREATE OR REPLACE EXTERNAL TABLE  vertexai-489303.newyork_ride_database.external_yellow_tripdata_2024
options (
  format = 'parquet',
  uris = ['gs://cohorts-data-warehouse/yellow_tripdata_2024-*.parquet']
);

select count(DISTINCT PULocationID) from vertexai-489303.newyork_ride_database.external_yellow_tripdata_2024;

select count(DISTINCT PULocationID) from vertexai-489303.newyork_ride_database.non_external_yellow_tripdata_2024;

select PULocationID from vertexai-489303.newyork_ride_database.non_external_yellow_tripdata_2024;
--155.12 mb 
select PULocationID,DOLocationID  from vertexai-489303.newyork_ride_database.non_external_yellow_tripdata_2024;


select count(*) from newyork_ride_database.non_external_yellow_tripdata_2024 WHERE fare_amount=0;



create or replace table vertexai-489303.newyork_ride_database.partition_yellow_tripdata_2024
partition by date(tpep_dropoff_datetime) 
cluster by VendorID
AS 
select * from vertexai-489303.newyork_ride_database.external_yellow_tripdata_2024;



select distinct VendorID from newyork_ride_database.non_external_yellow_tripdata_2024
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';


select distinct VendorID from newyork_ride_database.partition_yellow_tripdata_2024
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';