with source as (
    select * from {{ source('main', 'raw_weather') }}
),
renamed as (
    select
        -- The timestamp is passed as a string like "2026-03-24T00:00"
        CAST(time AS TIMESTAMP) as weather_timestamp,
        -- Temperature values
        CAST(temperature_2m AS FLOAT) as temperature_celsius
    from source
)
select * from renamed
