{{
    config(
        materialized='view'
    )
}}

with 

cycledata as (

    select 
        *, 
        row_number() over(partition by unqid, date_time, dir, mode, path) as rn
    from {{ source('staging', 'Inner_cycle_data') }}
    where unqid is not null

),

renamed as (

    select
        {{ dbt_utils.generate_surrogate_key(['unqid', 'date_time', 'dir', 'mode', 'path']) }} as cycle_id,
        date_time,
        year,
        unqid as locationid,
        weather,
        day,
        round,
        dir,
        path,
        mode,
        count,
        programme

    from cycledata
    where rn = 1
    and mode in ('Private cycles', 'Cycle hire bikes')
)

select * from renamed

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=false) %}

  limit 100

{% endif %}