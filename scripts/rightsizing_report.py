# Rightsizing and idle-resource report.
# Pulls EC2 rightsizing recommendations from Compute Optimizer and month-to-date
# spend from Cost Explorer, prints a summary, and optionally emails it via SNS.
import argparse
import datetime as dt

import boto3


def compute_optimizer_ec2(region):
    co = boto3.client("compute-optimizer", region_name=region)
    findings = []
    try:
        resp = co.get_ec2_instance_recommendations()
    except Exception as exc:
        print("Compute Optimizer not available or not enrolled:", exc)
        return findings
    for rec in resp.get("instanceRecommendations", []):
        options = rec.get("recommendationOptions", [])
        best = options[0] if options else {}
        findings.append({
            "instance": rec.get("instanceArn", "").split("/")[-1],
            "current": rec.get("currentInstanceType"),
            "recommended": best.get("instanceType"),
            "finding": rec.get("finding"),
        })
    return findings


def month_to_date_cost(region):
    ce = boto3.client("ce", region_name=region)
    today = dt.date.today()
    start = today.replace(day=1).isoformat()
    end = today.isoformat()
    if start == end:
        return []
    resp = ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )
    rows = []
    for group in resp["ResultsByTime"][0]["Groups"]:
        amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
        if amount > 0:
            rows.append((group["Keys"][0], round(amount, 2)))
    return sorted(rows, key=lambda r: r[1], reverse=True)


def main():
    parser = argparse.ArgumentParser(description="AWS rightsizing and cost report")
    parser.add_argument("--region", default="eu-central-1")
    parser.add_argument("--sns-topic-arn", default=None, help="Publish the report to this SNS topic")
    args = parser.parse_args()

    lines = ["AWS FinOps report - " + dt.date.today().isoformat(), ""]

    lines.append("Top services month-to-date:")
    for service, cost in month_to_date_cost(args.region)[:10]:
        lines.append("  {:40s} {:>10.2f} USD".format(service, cost))

    lines.append("")
    lines.append("EC2 rightsizing candidates:")
    recs = compute_optimizer_ec2(args.region)
    flagged = [r for r in recs if r["finding"] and r["finding"] != "OPTIMIZED"]
    if not flagged:
        lines.append("  none (all optimized or no data)")
    for r in flagged:
        lines.append("  {} {} -> {} ({})".format(r["instance"], r["current"], r["recommended"], r["finding"]))

    report = "\n".join(lines)
    print(report)

    if args.sns_topic_arn:
        boto3.client("sns", region_name=args.region).publish(
            TopicArn=args.sns_topic_arn, Subject="Weekly AWS FinOps report", Message=report
        )
        print("\nPublished to SNS.")


if __name__ == "__main__":
    main()
