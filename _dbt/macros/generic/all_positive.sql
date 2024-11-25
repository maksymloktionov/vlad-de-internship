{% macro test_all_positive(model, column_name) %}

WITH validation AS (
    SELECT {{ column_name }} AS test_sample
    FROM {{ model }}
)

SELECT *
FROM validation
WHERE test_sample < 0

{% endmacro %}