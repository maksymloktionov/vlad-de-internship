WITH goal_res AS (
    SELECT
        goal.id,
        goal.date,
        goal.home_team,
        goal.away_team,
        goal.scorer_team,
        goal.scorer,
        goal.minute,
        goal.is_own_goal,
        goal.is_penalty,
        res.home_score,
        res.away_score,
        res.tournament_name,
        res.city,
        res.country,
        res.neutral,
        res.winner
    FROM {{ ref("stg_raw__goalscorers") }} as goal
    LEFT JOIN {{ ref("stg_raw__results") }} as res
    ON goal.date = res.date AND
        goal.home_team = res.home_team AND
        goal.away_team = res.away_team
)

SELECT *
FROM goal_res
ORDER BY id