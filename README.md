# AWS FinOps Automation

Practical FinOps as code: **cost visibility** through Athena queries over the Cost and Usage Report (CUR), **tagging enforcement** with AWS Config, **budget and anomaly alerts** via Terraform, and a **Python rightsizing and idle-resource report** that emails a weekly summary.

> Maintained by [nrobertio](https://github.com/nrobertio). A generic, public version of the FinOps work I do day to day: tagging standards, rightsizing and anomaly detection to cut recurring cloud spend.

## What this demonstrates

- **Cost visibility**: reusable Athena SQL over the CUR (spend by service, by tag, untagged spend, month-over-month change).
- **Tagging governance**: an AWS Config rule that flags resources missing required cost-allocation tags.
- **Guardrails and alerts**: AWS Budgets with thresholds and a Cost Anomaly Detection monitor, in Terraform.
- **Actionable savings**: a Python job (Compute Optimizer + Cost Explorer) that lists rightsizing candidates and idle resources and emails the summary.

## Layout

```
terraform/     Budgets, Cost Anomaly Detection, tagging Config rule, SNS
athena/        CUR analysis queries (spend by service, by tag, untagged, MoM)
scripts/       Python rightsizing and idle-resource report (Compute Optimizer, Cost Explorer)
docs/          PROJECT.md: why, how, benefits, interview notes
```

## Usage

```bash
cd terraform && terraform init && terraform apply   # set alert_email, monthly_budget
python scripts/rightsizing_report.py --region eu-central-1
```

The Athena queries assume a CUR delivered to S3 and a Glue/Athena table; the query file documents the expected columns.

## License

MIT. See [LICENSE](LICENSE).
