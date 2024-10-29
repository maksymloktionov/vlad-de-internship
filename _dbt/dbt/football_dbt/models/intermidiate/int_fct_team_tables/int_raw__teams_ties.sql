SELECT 
    tnms.team_name,
    COALESCE(COUNT(CASE WHEN res.winner = 'Tie' THEN 1 END), 0) AS ties
FROM {{ ref("int_raw__teams") }} AS tnms
LEFT JOIN {{ ref("stg_raw__results") }} AS res
    ON tnms.team_name = res.away_team OR
       tnms.team_name = res.home_team
GROUP BY tnms.team_name