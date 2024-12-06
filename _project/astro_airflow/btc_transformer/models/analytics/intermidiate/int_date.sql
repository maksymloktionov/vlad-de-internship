SELECT
    date,
    HOUR(date) AS hour,
    DAY(date) AS day_of_month,
    MONTH(date) AS month,
    QUARTER(date) AS quarter,
    YEAR(date) AS year
FROM {{ ref('stg_date') }}