{% test less_than_n(model, column_name, n) %}
SELECT
    {{ column_name }} AS offending_value
FROM {{ model }}
WHERE {{ column_name }} >= {{ n }}
{% endtest %}
