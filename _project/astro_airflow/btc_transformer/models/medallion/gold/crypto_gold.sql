WITH gold AS (
    SELECT
        DATE(readable_time) AS date,
        AVG(open) AS avg_open,
        AVG(high) AS avg_high,
        AVG(low) AS avg_low,
        AVG(close) AS avg_close,
        SUM(volume) AS total_volume,
        SUM(number_of_trades) AS total_number_of_trades,
        SUM(taker_buy_base_asset) AS total_taker_buy_base,
        SUM(taker_buy_quote_asset) AS total_taker_buy_quote
    FROM {{ ref("crypto_silver") }}
    GROUP BY DATE(readable_time)
    ORDER BY date
)

SELECT *
FROM gold;
