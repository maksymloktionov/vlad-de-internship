SELECT
    ROW_NUMBER() OVER(ORDER BY date) AS id,
    DATE_FORMAT(date, "yyyy-MM-dd-H") AS date,
    hour,
    dayofyear(date) as day_of_year,
    day_of_month,
    date_part('dayofweek_iso', date) as day_of_week_i,
    month,
    quarter,
    year
FROM `crypto`.`default`.`int_date`