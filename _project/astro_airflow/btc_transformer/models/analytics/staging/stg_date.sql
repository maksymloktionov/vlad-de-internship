WITH all_date AS(
    SELECT
        readable_time AS date
    FROM {{ ref("crypto_silver") }}
    UNION ALL
    SELECT MAX(readable_time) + INTERVAL 1 HOUR
    FROM {{ ref("crypto_silver") }}
)

SELECT 
    DISTINCT *
FROM all_date

