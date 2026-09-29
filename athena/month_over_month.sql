-- Month-over-month cost per service to spot growth.
SELECT line_item_product_code AS service,
       date_trunc('month', line_item_usage_start_date) AS month,
       ROUND(SUM(line_item_unblended_cost), 2) AS cost_usd
FROM cur_table
WHERE line_item_usage_start_date >= date_add('month', -3, current_date)
GROUP BY line_item_product_code, date_trunc('month', line_item_usage_start_date)
ORDER BY service, month;
