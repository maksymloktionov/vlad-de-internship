SELECT
    ROW_NUMBER() OVER() as id,
    tournament_name,
    city,
    country
FROM {{ ref("int_raw__combinations") }}
GROUP BY tournament_name, city, country