{{
    config(
        materialized='table',
        partition_by={
        "field": "date_time",
        "data_type": "datetime",
        "granularity": "day"
        }
    )
}}
-- cluster_by = ["programme", "locationid","mode"],
with central_cycle_data as (
    select *
    from {{ ref('stg_central_cycle_data') }}
),
Inner_cycle_data as (
    select *
    from {{ ref('stg_Inner_cycle_data') }}
),
Outer_cycle_data as (
    select *
    from {{ ref('stg_Outer_cycle_data') }}
),
trips_unioned as (
    select * from central_cycle_data
    union all 
    select * from Inner_cycle_data
    union all 
    select * from Outer_cycle_data
), 
dim_locations as (
    select * from {{ ref('dim_locations') }}
    --where borough != 'Unknown'
)
select *
from trips_unioned
inner join dim_locations
on trips_unioned.locationid = dim_locations.Site_ID
-- testing CI job