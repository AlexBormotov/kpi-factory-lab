# Evidence WU-001

Команды с этой машины, 2026-09-09.

| команда | код | заметка |
|---|---|---|
| `python generate.py` | 0 | 15 кликов, 9 конверсий, 9 строк шаблона эталона |
| `python -m pytest -q` | 1 | **1 failed, 4 passed** — failed: «заполните эталон» |
| `python -m kpi.calculator` | 0 | `output/kpi.csv`, 9 строк |
| `python -m kpi.evidence` | 1 | пишет `output/pytest.json` (passed=4, failed=1) |
| `python -m kpi.report` | 0 | `output/dashboard.html` |

SHA калькулятора в отчёте: `9ac231d819b6` (первые 12 символов sha256 `kpi/calculator.py`).

`pytest.ini` задаёт `testpaths = tests`, иначе в оракул попадали тесты `ai-factory-kit/monitoring`.
