-- Top services by unblended cost, current month.
SELECT line_item_product_code AS service,
       ROUND(SUM(line_item_unblended_cost), 2) AS cost_usd
FROM cur_table
WHERE line_item_usage_start_date >= date_trunc('month', current_date)
GROUP BY line_item_product_code
ORDER BY cost_usd DESC
LIMIT 25;
