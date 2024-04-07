with 

source as (

    select * from {{ source('staging', 'cycle_data') }}

),

renamed as (

    select
        date_time,
        year,
        unqid,
        weather,
        day,
        round,
        dir,
        path,
        mode,
        count,
        programme

    from source

)

select * from renamed
