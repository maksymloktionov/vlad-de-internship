
  
    
        create or replace table `crypto`.`default`.`int_date`
      
      using delta
      
      
      
      
      
      
      
      as
      SELECT
    date,
    HOUR(date) AS hour,
    DAY(date) AS day_of_month,
    MONTH(date) AS month,
    QUARTER(date) AS quarter,
    YEAR(date) AS year
FROM `crypto`.`default`.`stg_date`
  