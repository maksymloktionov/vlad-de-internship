
  
    
        create or replace table `crypto`.`default`.`dim_symbol`
      
      using delta
      
      
      
      
      
      
      
      as
      WITH symbols AS(
    SELECT
        DISTINCT symbol
    FROM crypto_silver
)

SELECT
    ROW_NUMBER() OVER(ORDER BY symbol) AS id,
    *
FROM symbols
  