with staging as (
    select * from {{ ref('stg_weather') }}
),
daily_stats as (
    select
        CAST(weather_timestamp AS DATE) as date_day,
        MIN(temperature_celsius) as min_temperature_celsius,
        MAX(temperature_celsius) as max_temperature_celsius,
        AVG(temperature_celsius) as avg_temperature_celsius
    from staging
    group by 1
)
select * from daily_stats
