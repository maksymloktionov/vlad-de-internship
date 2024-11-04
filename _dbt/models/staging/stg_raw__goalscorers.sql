SELECT
    id,
    date,
    home_team,
    away_team,
    team AS scorer_team,
    scorer,
    minute,
    own_goal AS is_own_goal,
    penalty AS is_penalty
FROM {{ source("raw", "goalscorers") }}