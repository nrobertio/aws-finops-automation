-- Spend on resources missing the Project tag (tagging-gap cost).
SELECT line_item_product_code AS service,
       ROUND(SUM(line_item_unblended_cost), 2) AS untagged_cost_usd
FROM cur_table
WHERE (resource_tags_user_project IS NULL OR resource_tags_user_project = '')
  AND line_item_usage_start_date >= date_trunc('month', current_date)
GROUP BY line_item_product_code
ORDER BY untagged_cost_usd DESC;
