select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      SELECT
    <class 'dbt.adapters.databricks.column.DatabricksColumn'> AS offending_value
FROM 
WHERE <class 'dbt.adapters.databricks.column.DatabricksColumn'> >= 
      
    ) dbt_internal_test