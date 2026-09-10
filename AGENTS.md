# KPI-станок — договор с агентом

Учебный калькулятор. Не Kloud Data. Не байерский дашборд.

## Что это

Сырьё: `fixtures/clicks.csv`, `fixtures/conversions.csv`.
Счёт: Cost / Revenue / Profit / ROI, разрез campaign × day.
Оракул: pytest против `expected/kpi.csv`.

## Что можно менять

После первого `python generate.py` в рабочих циклах правь **только** `kpi/calculator.py`.

Не трогать: `generate.py`, `fixtures/`, `expected/`, `tests/`, `kpi/report.py`, `kpi/evidence.py`.

## Команды

```bash
pip install -r requirements.txt
python -m pytest -q
python -m pytest tests/test_kpi.py::test_kpi_matches_expected
python scripts/negative_control.py
python -m kpi.calculator
python -m kpi.evidence
python -m kpi.report
```

`python generate.py` не запускать, если эталон уже заполнен.

## Что какой файл кормит

| файл | гейт |
|---|---|
| `expected/kpi.csv` + `tests/test_kpi.py` | G4 оракул |
| `scripts/negative_control.py` | G4, строка 3.5 |
| `.github/workflows/ci.yml` job `test` | G7 |
| `.github/main-g7-ruleset.json` | G7, защита `main` |
| `docs/intent/REQ-*.md`, `WU-*.md` | G1 |
| `docs/runs/` | G6 |
| `docs/audit/gates.md` | посадка: можно ли без человека |
| `output/` | не в git; не оракул |

## Gotchas

- Все даты в данных — строки дат, без таймзоны. Учебный станок, не EST-пайплайн Kloud.
- Profit и ROI в эталон не пишут: их считают тесты.
- Прямой `git push origin main` отвергается. Ветка → PR → зелёный `test`.
- Unattended landing нет: G2, G5, G9 открыты.
