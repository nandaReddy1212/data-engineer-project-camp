with green_tripdata as (
    select * from {{ ref('stg_green_tripdate') }}
),

yellow_tripdata as (
    select * from {{ ref('stg_yellow_tripdate') }}
),

trips_unioned as (
    select * from green_tripdata
    union all
    select * from yellow_tripdata
)
select * from trips_unioned