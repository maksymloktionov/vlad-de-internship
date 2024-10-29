SELECT
    ROW_NUMBER() OVER () AS id,
    date
FROM (
    SELECT DISTINCT date
    FROM {{ ref('int_raw__combinations') }}
) AS distinct_dates
