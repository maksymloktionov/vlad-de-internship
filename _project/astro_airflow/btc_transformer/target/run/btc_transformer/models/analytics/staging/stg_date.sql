
  
    
        create or replace table `crypto`.`default`.`stg_date`
      
      using delta
      
      
      
      
      
      
      
      as
      WITH all_date AS(
    SELECT
        readable_time AS date
    FROM `crypto`.`default`.`crypto_silver`
    UNION ALL
    SELECT MAX(readable_time) + INTERVAL 1 HOUR
    FROM `crypto`.`default`.`crypto_silver`
)

SELECT 
    DISTINCT *
FROM all_date
  