"""Витрина только читает файлы. Сама pytest не запускает."""

from __future__ import annotations

import json
from pathlib import Path

from kpi.report import write_dashboard


def test_dashboard_renders_kpi_and_pytest_tables(tmp_path: Path) -> None:
    kpi_csv = tmp_path / "kpi.csv"
    pytest_json = tmp_path / "pytest.json"
    html_path = tmp_path / "dashboard.html"
    kpi_csv.write_text(
        "campaign,day,cost,revenue,profit,roi\n"
        "alpha,2026-09-01,10,20,10,1.0\n",
        encoding="utf-8",
    )
    pytest_json.write_text(
        json.dumps(
            {
                "passed": 2,
                "failed": 1,
                "sha": "aaa",
                "started_at": "2026-09-10T00:00:00",
            }
        ),
        encoding="utf-8",
    )

    write_dashboard(
        kpi_csv=kpi_csv,
        pytest_json=pytest_json,
        html_path=html_path,
        current_sha="bbb",
    )
    html = html_path.read_text(encoding="utf-8")
    assert "alpha" in html
    assert "2026-09-01" in html
    assert "улики устарели" in html
    assert "passed" in html or "прошло" in html
    assert "2" in html
    assert "1" in html
