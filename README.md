# KPI-станок (AI Factory lab)

Учебный калькулятор Cost / Revenue / Profit / ROI. Не продукт для байера.

## Что заморожено, что можно менять

После первого `python generate.py` агент в следующих циклах меняет **только** `kpi/calculator.py`.

Не трогать: `generate.py`, `fixtures/`, `expected/`, `tests/`, `kpi/report.py`, `kpi/evidence.py`.

Термины: [docs/GLOSSARY.md](docs/GLOSSARY.md). Intent: [docs/intent/REQ-001.md](docs/intent/REQ-001.md).

## Команды

```bash
python generate.py              # один раз; сотрёт эталон, если уже заполняли
python -m kpi.calculator         # output/kpi.csv
python -m pytest                # оракул
python -m kpi.evidence          # гоняет pytest и пишет output/pytest.json
python -m kpi.report            # output/dashboard.html — открыть в браузере
```

Зависимость: `pip install -r requirements.txt`.

CI: `.github/workflows/ci.yml` гоняет тот же pytest. Пока на GitHub не включена защита `main` («require status checks»), это **детектор**, не ворота G7. Ворота: `docs/audit/gates.md`.

## Как заполнить эталон

Файл `expected/kpi.csv`: одна строка = кампания × день.

- `cost` — сумма `cost` кликов этой пары, где `is_bot` не true
- `revenue` — сумма `payout` конверсий, где `type` равен `purchase`
- Profit и ROI не пишите

Подробнее: `expected/HOW-TO.md`.
