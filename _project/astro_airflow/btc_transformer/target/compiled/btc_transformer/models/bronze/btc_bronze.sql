WITH bronze AS (
    SELECT
        _c0 AS time,
        _c1 AS open,
        _c2 AS high,
        _c3 AS low,
        _c4 AS close,
        _c5 AS volume,
        _c6 AS close_time,
        _c7 AS quote_asset_volume,
        _c8 AS number_of_trades,
        _c9 AS taker_buy_base_asset,
        _c10 AS taker_buy_quote_asset,
        _c11 AS ignorance
    FROM btc_raw
)

SELECT *
FROM bronze