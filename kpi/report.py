"""Собирает HTML из уже посчитанных файлов. Не считает KPI и не гоняет pytest."""

from __future__ import annotations

import csv
import html
import json
from pathlib import Path

from kpi.evidence import current_code_sha

ROOT = Path(__file__).resolve().parents[1]


def write_dashboard(
    kpi_csv: Path,
    pytest_json: Path,
    html_path: Path,
    current_sha: str | None = None,
) -> None:
    html_path.parent.mkdir(parents=True, exist_ok=True)
    live_sha = current_sha if current_sha is not None else current_code_sha()
    kpi_rows = _read_csv(kpi_csv)
    report = _read_json(pytest_json)
    stale = report.get("sha") != live_sha
    stale_line = "<p class='stale'>улики устарели</p>" if stale else ""
    page = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>KPI станок</title>
  <style>
    body {{ font-family: sans-serif; margin: 24px; background: #fff; color: #111; }}
    table {{ border-collapse: collapse; margin-bottom: 24px; }}
    th, td {{ border: 1px solid #ccc; padding: 6px 10px; }}
    .stale {{ color: #b00; font-weight: bold; }}
  </style>
</head>
<body>
  <h1>KPI станок</h1>
  {stale_line}
  <h2>Таблица KPI</h2>
  {_table(kpi_rows, ["campaign", "day", "cost", "revenue", "profit", "roi"])}
  <h2>Последний pytest</h2>
  {_meta_table(report, live_sha)}
</body>
</html>
"""
    html_path.write_text(page, encoding="utf-8")


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {"passed": "", "failed": "", "sha": "", "started_at": ""}
    return json.loads(path.read_text(encoding="utf-8"))


def _table(rows: list[dict], columns: list[str]) -> str:
    head = "".join(f"<th>{html.escape(col)}</th>" for col in columns)
    body = []
    for row in rows:
        cells = "".join(f"<td>{html.escape(str(row.get(col, '')))}</td>" for col in columns)
        body.append(f"<tr>{cells}</tr>")
    return f"<table><tr>{head}</tr>{''.join(body)}</table>"


def _meta_table(report: dict, live_sha: str) -> str:
    rows = [
        ("passed (прошло)", report.get("passed", "")),
        ("failed (упало)", report.get("failed", "")),
        ("sha в отчёте", report.get("sha", "")),
        ("sha калькулятора сейчас", live_sha),
        ("started_at", report.get("started_at", "")),
    ]
    body = "".join(
        f"<tr><td>{html.escape(str(k))}</td><td>{html.escape(str(v))}</td></tr>" for k, v in rows
    )
    return f"<table>{body}</table>"


if __name__ == "__main__":
    write_dashboard(
        kpi_csv=ROOT / "output" / "kpi.csv",
        pytest_json=ROOT / "output" / "pytest.json",
        html_path=ROOT / "output" / "dashboard.html",
    )
    print(f"wrote {ROOT / 'output' / 'dashboard.html'}")
