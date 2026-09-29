# CUR analysis queries

These run against the Cost and Usage Report (CUR) exposed as an Athena table (via the AWS-provided Glue crawler or CUR Athena integration). Replace `cur_table` with your table name. Key columns used: `line_item_product_code`, `line_item_unblended_cost`, `line_item_usage_start_date`, and `resource_tags_user_*` for tag-based views.
