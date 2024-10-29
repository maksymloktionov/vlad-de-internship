SELECT
    ROW_NUMBER() OVER () AS id,
    tnms.team_name,
    wn.wins,
    ls.loses,
    ts.ties,
    gls.total_goals
FROM {{ ref("int_raw__teams") }} as tnms
INNER JOIN {{ ref("int_raw__teams_wins") }} as wn
ON tnms.team_name = wn.team_name
INNER JOIN {{ ref("int_raw__teams_loses") }} as ls
ON tnms.team_name = ls.team_name
INNER JOIN {{ ref("int_raw__teams_ties") }} as ts
ON tnms.team_name = ts.team_name
INNER JOIN {{ ref("int_raw__teams_goals") }} as gls
ON tnms.team_name = gls.team_name
