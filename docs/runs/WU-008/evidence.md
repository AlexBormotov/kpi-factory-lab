# Evidence WU-008

## До / после прогона

| файл | sha256 (git blob) до | после |
|---|---|---|
| `kpi/calculator.py` | `5f52ab1a27fb054b3b932e2aeb8f7eff4cab1079` | тот же |
| `expected/kpi.csv` | `360e3fbf688f8a61457a0f36013683a200249ad1` | тот же |

`python -m pytest -q` → 5 passed (оракул, не Claude).

## Маршрут

| | |
|---|---|
| Адаптер | Cursor Task `claude-thinking` |
| Определение | `.claude/agents/claude-thinking.md` / `.cursor/agents/claude-thinking.md` |
| CLI | `claude` 2.1.260, `claude auth status` loggedIn, Max |
| Режим | plan, opus, без записи (как в определении агента) |
| Код выхода адаптера | 0 (ответ получен) |
| Agent id | `ea1289d0-54cc-4c05-8d71-57b2fb1f5031` |

## Ответ Claude (дословно)

Все шесть файлов на месте.

1. **Оракул — `python -m pytest` против `expected/kpi.csv`.** Прямо сказано в `AGENTS.md:9` («Оракул: pytest против `expected/kpi.csv`») и в таблице гейтов `AGENTS.md:35` (`expected/kpi.csv` + `tests/test_kpi.py` = G4). Механика в `tests/test_kpi.py:16-51`: Cost/Revenue сверяются с эталоном, а Profit/ROI тест пересчитывает сам по формулам AC-4 (`docs/intent/REQ-001.md:20-21`). Пока эталон пустой — сюита падает с «заполните эталон» (`tests/test_kpi.py:19,25,33`).

2. **Нет, я не могу писать `expected/kpi.csv`.** Причины из файлов: `docs/intent/REQ-001.md:19` (AC-3) — «Числа эталона пишет только человек»; `docs/intent/REQ-001.md:30` — вне скоупа «LLM как автор эталона или как оракул (`claude-thinking` не пишет `kpi.csv`)»; `AGENTS.md:15` — `expected/` в списке «не трогать»; `AGENTS.md:53,56` — Claude CLI это «второй читатель, не оракул», «не писать `expected/`, `tests/`, `kpi/calculator.py`»; `docs/intent/REQ-003.md:16` (AC-2) требует, чтобы после прогона `expected/kpi.csv` и `kpi/calculator.py` были те же, что до него. Файл сейчас заполнен человеком (`expected/kpi.csv:2-10`), и при расхождении моего мнения с pytest побеждает pytest (`AGENTS.md:57`).

3. **Только `kpi/calculator.py`.** `AGENTS.md:13`: «После первого `python generate.py` в рабочих циклах правь **только** `kpi/calculator.py`»; то же в `docs/intent/REQ-001.md:24` (AC-8) — генератор, фикстуры, эталон, тесты и report заморожены; сам файл это подтверждает своим докстрингом `kpi/calculator.py:1` («Это edit surface агента»). Заморожены `generate.py`, `fixtures/`, `expected/`, `tests/`, `kpi/report.py`, `kpi/evidence.py` (`AGENTS.md:15`). Оговорка: это edit surface агента-калькулятора; для меня как second-opinion и он закрыт (`AGENTS.md:56`).

Pytest я не запускал и не запускаю — я не оракул; всё выше прочитано из файлов.
