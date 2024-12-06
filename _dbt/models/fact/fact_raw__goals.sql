SELECT
    ROW_NUMBER() OVER() as id,
    date.id as date_id,
    mtch.id as match_id,
    team.id as team_id,
    trnm.id as tournament_id,
    comb.scorer as player_name,
    comb.minute,
    comb.is_own_goal,
    comb.is_penalty
FROM {{ ref("int_raw__combinations") }} as comb
LEFT JOIN {{ ref("dim_raw__matches") }} as mtch
ON comb.home_team = mtch.home_team
    AND comb.away_team = mtch.away_team
    AND comb.winner = mtch.winner
    AND comb.home_score = mtch.home_score
    AND comb.away_score = mtch.away_score
    AND comb.neutral = mtch.neutral
LEFT JOIN {{ ref("dim_raw__teams") }} as team
ON comb.scorer_team = team.team_name
LEFT JOIN {{ ref('dim_raw__tournament') }} as trnm
ON comb.tournament_name = trnm.tournament_name
    AND comb.city = trnm.city
    AND comb.country = trnm.country
LEFT JOIN {{ ref("dim_raw__date") }} as date
ON comb.date = date.date