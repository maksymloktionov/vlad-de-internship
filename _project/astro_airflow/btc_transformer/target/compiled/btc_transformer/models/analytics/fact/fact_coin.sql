WITH all_in_one AS (
    SELECT
        date_one.id AS open_time_id,
        date_two.id AS close_time_id,
        symb.id AS symbol_id,
        source.*
    FROM `crypto`.`default`.`crypto_silver` AS source
    LEFT JOIN `crypto`.`default`.`dim_date` AS date_one
        ON DATE_FORMAT(source.readable_time, 'yyyy-MM-dd-H') = date_one.date
    LEFT JOIN `crypto`.`default`.`dim_date` AS date_two
        ON DATE_FORMAT(source.readable_close_time + INTERVAL 1 HOUR, 'yyyy-MM-dd-H') = date_two.date
    LEFT JOIN `crypto`.`default`.`dim_symbol` AS symb
        ON source.symbol = symb.symbol
)
SELECT
    ROW_NUMBER() OVER(ORDER BY symbol_id) AS id,
    open_time_id,
    close_time_id,
    symbol_id,
    open,
    high,
    low,
    close,
    volume,
    number_of_trades,
    taker_buy_base_asset,
    taker_buy_quote_asset
FROM all_in_one