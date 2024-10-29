WITH away_stat AS (
    SELECT
        tnms.team_name,
        COALESCE(SUM(res.away_score), 0) AS total_away_score
    FROM {{ ref("int_raw__teams") }} AS tnms
    LEFT JOIN {{ ref("stg_raw__results") }} AS res
    ON tnms.team_name = res.away_team
    GROUP BY tnms.team_name
),
home_stat AS (
    SELECT
        tnms.team_name,
        COALESCE(SUM(res.home_score), 0) AS total_home_score
    FROM {{ ref("int_raw__teams") }} AS tnms
    LEFT JOIN {{ ref("stg_raw__results") }} AS res
    ON tnms.team_name = res.home_team
    GROUP BY tnms.team_name
)

SELECT
    tnms.team_name,
    SUM(away.total_away_score + home.total_home_score) AS total_goals
FROM {{ ref("int_raw__teams") }} AS tnms
INNER JOIN away_stat AS away
ON tnms.team_name = away.team_name
INNER JOIN home_stat AS home
ON tnms.team_name = home.team_name
GROUP BY tnms.team_name