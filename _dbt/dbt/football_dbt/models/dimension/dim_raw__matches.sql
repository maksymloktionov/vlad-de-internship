SELECT
    ROW_NUMBER() OVER() as id,
    home_team,
    away_team,
    home_score,
    away_score,
    winner,
    neutral
FROM {{ ref('int_raw__combinations') }}
GROUP BY home_team,
         away_team,
         winner,
         away_score,
         home_score,
         neutral