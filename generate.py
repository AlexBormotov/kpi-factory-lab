"""Один раз создаёт сырые CSV и пустой шаблон эталона. Потом не трогать."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"
EXPECTED = ROOT / "expected"

# Жёсткий набор: 3 кампании, 3 дня, лимиты 30/15. Без random — эталон привязан к этим строкам.
CLICKS = [
    # alpha 01: валидные клики
    {"campaign": "alpha", "day": "2026-09-01", "cost": "10", "is_bot": "false"},
    {"campaign": "alpha", "day": "2026-09-01", "cost": "4", "is_bot": "false"},
    {"campaign": "alpha", "day": "2026-09-01", "cost": "3", "is_bot": "true"},
    {"campaign": "alpha", "day": "2026-09-02", "cost": "8", "is_bot": "false"},
    {"campaign": "alpha", "day": "2026-09-02", "cost": "2", "is_bot": "true"},
    {"campaign": "alpha", "day": "2026-09-03", "cost": "6", "is_bot": "false"},
    # beta: 01 только клики (нет конверсий); 02 боты; 03 валид
    {"campaign": "beta", "day": "2026-09-01", "cost": "5", "is_bot": "false"},
    {"campaign": "beta", "day": "2026-09-01", "cost": "1", "is_bot": "true"},
    {"campaign": "beta", "day": "2026-09-02", "cost": "7", "is_bot": "true"},
    {"campaign": "beta", "day": "2026-09-03", "cost": "9", "is_bot": "false"},
    {"campaign": "beta", "day": "2026-09-03", "cost": "3", "is_bot": "false"},
    # gamma 01: только боты (покупка без валидных кликов); 02–03 обычные
    {"campaign": "gamma", "day": "2026-09-01", "cost": "12", "is_bot": "true"},
    {"campaign": "gamma", "day": "2026-09-02", "cost": "11", "is_bot": "false"},
    {"campaign": "gamma", "day": "2026-09-03", "cost": "2", "is_bot": "false"},
    {"campaign": "gamma", "day": "2026-09-03", "cost": "4", "is_bot": "false"},
]

CONVERSIONS = [
    {"campaign": "alpha", "day": "2026-09-01", "payout": "20", "type": "purchase"},
    {"campaign": "alpha", "day": "2026-09-01", "payout": "5", "type": "lead"},
    {"campaign": "alpha", "day": "2026-09-02", "payout": "15", "type": "purchase"},
    {"campaign": "alpha", "day": "2026-09-03", "payout": "8", "type": "purchase"},
    {"campaign": "beta", "day": "2026-09-03", "payout": "12", "type": "purchase"},
    {"campaign": "beta", "day": "2026-09-03", "payout": "3", "type": "lead"},
    # покупка в день, где у gamma нет валидных кликов (только бот 09-01)
    {"campaign": "gamma", "day": "2026-09-01", "payout": "18", "type": "purchase"},
    {"campaign": "gamma", "day": "2026-09-02", "payout": "10", "type": "purchase"},
    {"campaign": "gamma", "day": "2026-09-03", "payout": "4", "type": "click"},
]


def _write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_expected_template(clicks: list[dict], conversions: list[dict], path: Path) -> None:
    """Ключи campaign×day из обоих файлов. Цифры не заполняем — это работа человека."""
    keys = sorted(
        {(row["campaign"], row["day"]) for row in clicks}
        | {(row["campaign"], row["day"]) for row in conversions}
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["campaign", "day", "cost", "revenue"])
        writer.writeheader()
        for campaign, day in keys:
            writer.writerow({"campaign": campaign, "day": day, "cost": "", "revenue": ""})


def main() -> None:
    assert len(CLICKS) <= 30
    assert len(CONVERSIONS) <= 15
    _write_csv(FIXTURES / "clicks.csv", CLICKS, ["campaign", "day", "cost", "is_bot"])
    _write_csv(FIXTURES / "conversions.csv", CONVERSIONS, ["campaign", "day", "payout", "type"])
    write_expected_template(CLICKS, CONVERSIONS, EXPECTED / "kpi.csv")
    print(f"clicks={len(CLICKS)} conversions={len(CONVERSIONS)}")
    print(f"wrote {FIXTURES / 'clicks.csv'}")
    print(f"wrote {FIXTURES / 'conversions.csv'}")
    print(f"wrote empty template {EXPECTED / 'kpi.csv'}")


if __name__ == "__main__":
    main()
