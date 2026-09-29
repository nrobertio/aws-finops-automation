-- Cost grouped by the Project cost-allocation tag.
SELECT COALESCE(NULLIF(resource_tags_user_project, ''), 'untagged') AS project,
       ROUND(SUM(line_item_unblended_cost), 2) AS cost_usd
FROM cur_table
WHERE line_item_usage_start_date >= date_trunc('month', current_date)
GROUP BY COALESCE(NULLIF(resource_tags_user_project, ''), 'untagged')
ORDER BY cost_usd DESC;
