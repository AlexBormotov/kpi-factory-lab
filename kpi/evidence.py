"""Улика последнего pytest. Не оракул: не решает, правильные ли KPI."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALCULATOR = ROOT / "kpi" / "calculator.py"


def current_code_sha() -> str:
    """SHA поверхности правок (калькулятор), не всего репозитория."""
    data = CALCULATOR.read_bytes() if CALCULATOR.exists() else b""
    return hashlib.sha256(data).hexdigest()[:12]


def write_pytest_report(
    pytest_args: list[str] | None = None,
    report_path: Path | None = None,
) -> int:
    report_path = report_path or (ROOT / "output" / "pytest.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    args = pytest_args or ["-q"]
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    # pytest --co -q не даёт счётчики в простом виде; парсим summary из stdout.
    passed, failed = _parse_counts(proc.stdout + proc.stderr)
    payload = {
        "passed": passed,
        "failed": failed,
        "sha": current_code_sha(),
        "started_at": started,
        "exit_code": proc.returncode,
    }
    report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    print(f"wrote {report_path}")
    return proc.returncode


def _parse_counts(text: str) -> tuple[int, int]:
    """Достаёт passed/failed из хвоста pytest. Формат: '5 passed, 1 failed in 0.20s'."""
    passed = failed = 0
    for raw in text.splitlines():
        tokens = raw.replace(",", "").split()
        for i, token in enumerate(tokens):
            if token in {"passed", "failed", "error", "errors"} and i > 0 and tokens[i - 1].isdigit():
                n = int(tokens[i - 1])
                if token == "passed":
                    passed = n
                else:
                    failed += n
    return passed, failed


if __name__ == "__main__":
    raise SystemExit(write_pytest_report())
