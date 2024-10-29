SELECT home_team AS team_name
FROM {{ ref("int_raw__combinations") }}
UNION
SELECT away_team AS team_name
FROM {{ ref('int_raw__combinations') }}
