"""Считает Cost / Revenue / Profit / ROI. Это edit surface агента."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Optional


def _is_bot(value: str) -> bool:
    return value.strip().lower() == "true"


def _empty_bucket() -> dict:
    return {"cost": 0.0, "revenue": 0.0}


def calculate_kpi(clicks_path: Path, conversions_path: Path) -> list[dict]:
    """Одна строка результата = одна пара campaign × day."""
    buckets: dict[tuple[str, str], dict] = defaultdict(_empty_bucket)

    with clicks_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            key = (row["campaign"], row["day"])
            buckets[key]
            if not _is_bot(row["is_bot"]):
                buckets[key]["cost"] += float(row["cost"])

    with conversions_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            key = (row["campaign"], row["day"])
            buckets[key]
            if row["type"] == "purchase":
                buckets[key]["revenue"] += float(row["payout"])

    result: list[dict] = []
    for campaign, day in sorted(buckets):
        cost = buckets[(campaign, day)]["cost"]
        revenue = buckets[(campaign, day)]["revenue"]
        profit = revenue - cost
        roi: Optional[float] = profit / cost if cost > 0 else None
        result.append(
            {
                "campaign": campaign,
                "day": day,
                "cost": cost,
                "revenue": revenue,
                "profit": profit,
                "roi": roi,
            }
        )
    return result


def write_kpi_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["campaign", "day", "cost", "revenue", "profit", "roi"]
        )
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["roi"] = "" if row["roi"] is None else round(row["roi"], 4)
            writer.writerow(out)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    table = calculate_kpi(root / "fixtures" / "clicks.csv", root / "fixtures" / "conversions.csv")
    write_kpi_csv(table, root / "output" / "kpi.csv")
    print(f"wrote {root / 'output' / 'kpi.csv'} ({len(table)} rows)")
