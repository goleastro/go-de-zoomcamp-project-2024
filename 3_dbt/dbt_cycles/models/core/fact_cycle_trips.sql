{{
    config(
        materialized='table',
        partition_by={
        "field": "date_time",
        "data_type": "datetime",
        "granularity": "day"
        }
        cluster_by = "mode",
    )
}}
-- cluster_by = ["programme", "locationid","mode"],
with central_cycle_data as (
    select cycle_id
            ,date_time
            ,year
            ,locationid
            ,weather	
            ,day
            ,round	
            ,dir		
            ,path	
            ,mode	
            ,count	
            ,programme
    from {{ ref('stg_central_cycle_data') }}
),
Inner_cycle_data as (
    select cycle_id
            ,date_time
            ,year
            ,locationid
            ,weather	
            ,day
            ,round	
            ,dir		
            ,path	
            ,mode	
            ,count	
            ,programme
    from {{ ref('stg_Inner_cycle_data') }}
),
Outer_cycle_data as (
    select cycle_id
            ,date_time
            ,year
            ,locationid
            ,weather	
            ,day
            ,round	
            ,dir		
            ,path	
            ,mode	
            ,count	
            ,programme
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
    select Site_ID			
            ,Location		
            ,Borough			
            ,Functional_area	
            ,Road_type 
    from {{ ref('dim_locations') }}
    --where borough != 'Unknown'
)
select trips_unioned.cycle_id
    ,trips_unioned.date_time
    ,trips_unioned.year	
    ,trips_unioned.locationid
    ,dim_locations.Location
    ,dim_locations.Borough
    ,dim_locations.Road_type
    ,trips_unioned.programme
    ,trips_unioned.weather	
    ,trips_unioned.day	
    ,trips_unioned.round	
    ,trips_unioned.dir		
    ,trips_unioned.path	
    ,trips_unioned.mode	
    ,trips_unioned.count	
from trips_unioned
inner join dim_locations
on trips_unioned.locationid = dim_locations.Site_ID
-- testing CI job