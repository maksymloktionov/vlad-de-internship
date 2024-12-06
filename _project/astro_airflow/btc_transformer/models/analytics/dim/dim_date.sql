SELECT
    ROW_NUMBER() OVER(ORDER BY date) AS id,
    DATE_FORMAT(date, "yyyy-MM-dd-H") AS date,
    hour,
    {{ dbt_date.day_of_year("date") }} as day_of_year,
    day_of_month,
    {{ dbt_date.day_of_week("date") }} as day_of_week_i,
    month,
    quarter,
    year
FROM {{ ref("int_date") }}