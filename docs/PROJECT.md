# Project Writeup: AWS FinOps Automation

Why this exists, how it was built, why each choice, and the benefits. Also the interview talking-track.

## 1. The problem it solves

Cloud bills grow quietly. Nobody decides to overspend; it accumulates from idle instances, oversized resources, untagged spend nobody can attribute, and gradual creep that no single person notices. FinOps is the practice of making cost visible, attributable and controllable. This project automates the four things that deliver most of the savings: visibility, tagging discipline, alerting, and concrete rightsizing actions.

## 2. How it was built

- Visibility (athena/): reusable SQL over the Cost and Usage Report, spend by service, spend by the Project tag, untagged spend, and month-over-month growth.
- Tagging governance (terraform/tagging.tf): an AWS Config REQUIRED_TAGS rule that flags any resource missing the cost-allocation tags, so untagged spend gets caught at source.
- Guardrails and alerts (terraform/): AWS Budgets with an 80 percent actual and 100 percent forecast alert, plus a Cost Anomaly Detection monitor that emails when an anomaly crosses a dollar threshold.
- Actionable savings (scripts/): a Python job that pulls EC2 rightsizing recommendations from Compute Optimizer and month-to-date spend from Cost Explorer, then prints and optionally SNS-emails a summary.

## 3. Why each choice

- CUR over the Cost Explorer console: the CUR is the most granular, penny-accurate source, and Athena lets you slice it any way, including by tag, which the console does poorly.
- Tagging enforced with Config, not hoped for: untagged spend is unattributable spend. A REQUIRED_TAGS rule turns tagging from a guideline into a measurable compliance number.
- Budgets and Anomaly Detection together: budgets catch the slow creep against a known limit; anomaly detection catches sudden unexpected spikes a fixed budget would miss. You want both.
- Compute Optimizer for rightsizing: it uses real utilization metrics rather than guesses, so the recommendations are defensible when you ask a team to downsize.
- A report that emails itself: FinOps only works if the numbers reach people regularly. A weekly SNS summary beats a dashboard nobody opens.

## 4. Benefits

- Spend becomes attributable: every dollar maps to a project and owner, or it is flagged.
- Slow creep and sudden spikes are both alerted, not discovered on the invoice.
- Rightsizing candidates are surfaced with evidence, turning cost talk into specific actions.
- All of it is code: the guardrails are version-controlled and reproducible across accounts.

## 5. Interview talking points

- CUR vs Cost Explorer vs Budgets: CUR is the raw granular data (Athena), Cost Explorer is the query and forecasting API, Budgets is the alerting guardrail. This project uses all three for what each does best.
- Why tagging is the foundation of FinOps: without it, no showback or chargeback is possible and optimization is blind.
- Budgets vs Anomaly Detection: fixed-threshold vs statistical-baseline alerting; they catch different failure modes.
- How you would drive savings from this: start with untagged spend and idle resources (fast wins), then rightsizing, then commitment discipline (Savings Plans and Reserved Instances).
- What to add next: automated Savings Plans coverage reporting, scheduled stop/start for non-prod, and per-team budgets wired to the tagging standard.

## 6. How to run it

```bash
cd terraform
terraform init
terraform apply   # set alert_email and monthly_budget, then confirm the SNS email

python scripts/rightsizing_report.py --region eu-central-1 --sns-topic-arn <finops_topic_arn>
```

The Athena queries expect a CUR table; see athena/README.md for the columns used.