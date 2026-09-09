"""Negative control оракула: ломаем фильтр ботов, смотрим, кто краснеет.

Правило: в production-коде отключаем поведение, гоняем pytest.
Тесты про Cost должны упасть. Тесты про CSV-лимиты и HTML — нет.
Потом файл калькулятора всегда возвращаем как был.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALCULATOR = ROOT / "kpi" / "calculator.py"

# Уникальный кусок, который и есть фильтр. Его временно выкидываем.
NEEDLE = """            if not _is_bot(row["is_bot"]):
                buckets[key]["cost"] += float(row["cost"])
"""
BROKEN = """            buckets[key]["cost"] += float(row["cost"])
"""

MUST_FAIL = [
    "tests/test_kpi.py::test_calculator_filters_and_groups",
    "tests/test_kpi.py::test_kpi_matches_expected",
]
MUST_PASS = [
    "tests/test_generate.py",
    "tests/test_report.py",
]


def _run(args: list[str]) -> int:
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", *args], cwd=ROOT)
    return proc.returncode


def main() -> int:
    # Читаем оригинал один раз. В finally всегда пишем его обратно.
    original = CALCULATOR.read_text(encoding="utf-8")
    if NEEDLE not in original:
        print("FAIL: bot-filter needle not found in calculator.py")
        return 2
    try:
        # Один replace: фильтр выключен, cost плюсуется всегда.
        CALCULATOR.write_text(original.replace(NEEDLE, BROKEN, 1), encoding="utf-8")
        fail_code = _run(MUST_FAIL)
        pass_code = _run(MUST_PASS)
    finally:
        CALCULATOR.write_text(original, encoding="utf-8")

    # 0 у pytest = все зелёные. Нам нужно наоборот: Cost должен упасть.
    if fail_code == 0:
        print("FAIL: bot filter off, but Cost tests still green")
        return 1
    if pass_code != 0:
        print("FAIL: unrelated tests (generate/HTML) went red")
        return 1
    print("ok: Cost tests red, generate and HTML green, calculator restored")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
