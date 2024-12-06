SELECT
    id,
    date,
    home_team,
    away_team,
    home_score,
    away_score,
    tournament as tournament_name,
    city,
    country,
    neutral,
    CASE
        WHEN home_score > away_score THEN home_team
        WHEN away_score > home_score THEN away_team
        ELSE 'Tie'
    END AS winner
FROM {{ source("raw", "results") }}