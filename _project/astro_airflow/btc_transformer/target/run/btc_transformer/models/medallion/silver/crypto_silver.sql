
  
    
        create or replace table `crypto`.`default`.`crypto_silver`
      
      using delta
      
      
      
      
      
      
      
      as
      WITH silver AS (
    SELECT
        CAST(FROM_UNIXTIME(time / 1000) AS TIMESTAMP) AS readable_time,
        CAST(open AS DOUBLE) AS open,
        CAST(high AS DOUBLE) AS high,
        CAST(low AS DOUBLE) AS low,
        CAST(close AS DOUBLE) AS close,
        CAST(volume AS DOUBLE) AS volume,
        CAST(FROM_UNIXTIME(close_time / 1000) AS TIMESTAMP) AS readable_close_time,
        CAST(number_of_trades AS INT) AS number_of_trades,
        CAST(taker_buy_base_asset AS DOUBLE) AS taker_buy_base_asset,
        CAST(taker_buy_quote_asset AS DOUBLE) AS taker_buy_quote_asset,
        symbol
    FROM `crypto`.`default`.`crypto_bronze`
)

SELECT *
FROM silver
  