"""Проверки замороженных CSV. Тесты не запускают generate.py — иначе сотрут эталон."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_generate_writes_csv_within_caps() -> None:
    clicks = list(csv.DictReader((ROOT / "fixtures" / "clicks.csv").open(encoding="utf-8")))
    convs = list(csv.DictReader((ROOT / "fixtures" / "conversions.csv").open(encoding="utf-8")))
    assert 1 <= len(clicks) <= 30
    assert 1 <= len(convs) <= 15
    campaigns = {row["campaign"] for row in clicks} | {row["campaign"] for row in convs}
    days = {row["day"] for row in clicks} | {row["day"] for row in convs}
    assert len(campaigns) <= 3
    assert len(days) <= 3


def test_generate_has_required_diversity() -> None:
    clicks = list(csv.DictReader((ROOT / "fixtures" / "clicks.csv").open(encoding="utf-8")))
    convs = list(csv.DictReader((ROOT / "fixtures" / "conversions.csv").open(encoding="utf-8")))

    assert any(row["is_bot"].lower() == "true" for row in clicks)
    assert any(row["type"] != "purchase" for row in convs)

    click_keys = {(row["campaign"], row["day"]) for row in clicks}
    conv_keys = {(row["campaign"], row["day"]) for row in convs}
    assert click_keys - conv_keys, "нужен день только с кликами"

    valid_click_keys = {
        (row["campaign"], row["day"])
        for row in clicks
        if row["is_bot"].lower() != "true"
    }
    purchase_keys = {
        (row["campaign"], row["day"])
        for row in convs
        if row["type"] == "purchase"
    }
    assert purchase_keys - valid_click_keys, "нужна покупка без валидных кликов"
