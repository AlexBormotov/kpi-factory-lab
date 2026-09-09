"""Оракул и каркас станка. Пока эталон пустой — этот файл должен краснеть."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from kpi.calculator import calculate_kpi

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ROOT / "expected" / "kpi.csv"


def test_kpi_matches_expected() -> None:
    """AC-5: пустой эталон → «заполните эталон». Заполненный → сверка с калькулятором."""
    if not EXPECTED.exists():
        pytest.fail("заполните эталон: нет файла expected/kpi.csv")

    with EXPECTED.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        pytest.fail("заполните эталон: в expected/kpi.csv нет строк")

    empty = [
        row
        for row in rows
        if not (row.get("cost") or "").strip() or not (row.get("revenue") or "").strip()
    ]
    if empty:
        pytest.fail("заполните эталон: пустые cost/revenue в expected/kpi.csv")

    # Эталон заполнен человеком. Сверяем с калькулятором (Cost/Revenue)
    # и пересчитываем Profit/ROI сами — агент не пишет эти поля в эталон.
    actual = {
        (row["campaign"], row["day"]): row
        for row in calculate_kpi(ROOT / "fixtures" / "clicks.csv", ROOT / "fixtures" / "conversions.csv")
    }
    for row in rows:
        key = (row["campaign"], row["day"])
        got = actual[key]
        want_cost = float(row["cost"])
        want_revenue = float(row["revenue"])
        assert got["cost"] == want_cost
        assert got["revenue"] == want_revenue
        profit = want_revenue - want_cost
        assert got["profit"] == profit
        want_roi = profit / want_cost if want_cost > 0 else None
        assert got["roi"] == want_roi


def test_calculator_filters_and_groups(tmp_path: Path) -> None:
    """AC-4: боты не в Cost, не-purchase не в Revenue, срез campaign × day."""
    clicks = tmp_path / "clicks.csv"
    convs = tmp_path / "conversions.csv"
    clicks.write_text(
        "campaign,day,cost,is_bot\n"
        "alpha,2026-09-01,10,false\n"
        "alpha,2026-09-01,5,true\n"
        "beta,2026-09-01,4,false\n"
        "beta,2026-09-02,9,true\n",
        encoding="utf-8",
    )
    convs.write_text(
        "campaign,day,payout,type\n"
        "alpha,2026-09-01,20,purchase\n"
        "alpha,2026-09-01,7,lead\n"
        "gamma,2026-09-02,9,purchase\n",
        encoding="utf-8",
    )

    table = { (r["campaign"], r["day"]): r for r in calculate_kpi(clicks, convs) }

    alpha = table[("alpha", "2026-09-01")]
    assert alpha["cost"] == 10.0
    assert alpha["revenue"] == 20.0
    assert alpha["profit"] == 10.0
    assert alpha["roi"] == 1.0

    beta = table[("beta", "2026-09-01")]
    assert beta["cost"] == 4.0
    assert beta["revenue"] == 0.0
    assert beta["profit"] == -4.0
    assert beta["roi"] == -1.0

    beta_bot_day = table[("beta", "2026-09-02")]
    assert beta_bot_day["cost"] == 0.0
    assert beta_bot_day["revenue"] == 0.0
    assert beta_bot_day["roi"] is None

    gamma = table[("gamma", "2026-09-02")]
    assert gamma["cost"] == 0.0
    assert gamma["revenue"] == 9.0
    assert gamma["profit"] == 9.0
    assert gamma["roi"] is None
