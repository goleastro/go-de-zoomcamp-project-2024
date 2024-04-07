{{
    config(
        materialized='table'
    )
}}

with central_cycle_data as (
    select *
    from {{ ref('stg_central_cycle_data') }}
),
-- union your cycle data
--trips_unioned as (
--    select * from green_tripdata
--    union all 
--    select * from yellow_tripdata
--), 
dim_locations as (
    select * from {{ ref('dim_locations') }}
    --where borough != 'Unknown'
)
select *
from central_cycle_data
inner join dim_locations
on central_cycle_data.locationid = dim_locations.Site_ID