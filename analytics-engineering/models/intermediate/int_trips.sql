with unioned as (
    select * from {{ ref('int_trips_unioned') }}
),

payment_types as (
    select * from {{ ref('payment_type_lookup') }}
),



cleaned_and_enriched as (
    select
        {{ dbt_utils.generate_surrogate_key(['vendor_id', 'pickup_datetime', 'dropoff_datetime','pickup_location_id','dropoff_location_id']) }} as trip_id,
        u.vendor_id,
        u.rate_code_id,
        u.pickup_location_id,
        u.dropoff_location_id,
        u.pickup_datetime,
        u.dropoff_datetime,
        u.store_and_fwd_flag,
        u.passenger_count,
        u.trip_distance,
        u.trip_type,
        u.fare_amount,
        u.extra,
        u.mta_tax,
        u.tip_amount,
        u.tolls_amount,
        u.ehail_fee,
        u.improvement_surcharge,
        u.total_amount,
        Coalesce(u.payment_type, 0) as payment_type,  -- Handle null payment types by treating them as 'Unknown' (code 0)
        Coalesce(pt.description, 'Unknown') as payment_type_description,  -- Enrich with payment type description
        u.service_type
    from unioned u
    left join payment_types as pt
    on Coalesce(u.payment_type, 0) = pt.payment_type_code
)