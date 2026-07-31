from __future__ import annotations

import json
import math
import os
import shutil
from pathlib import Path


ROOT = Path(os.environ.get("BENCH_TASK_ROOT", "/root"))
LOGS = Path(os.environ.get("BENCH_VERIFIER_LOGS", "/logs/verifier"))


def load_result() -> dict[str, object]:
    path = ROOT / "result.json"
    assert path.is_file(), "Missing /root/result.json"
    result = json.loads(path.read_text())
    assert set(result) == {"d2", "d3"}
    for name in ("d2", "d3"):
        assert isinstance(result[name], (int, float))
        assert not isinstance(result[name], bool)
        assert math.isfinite(float(result[name]))
    LOGS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, LOGS / "submitted_result.json")
    return result


def test_result_schema() -> None:
    load_result()


def test_d2() -> None:
    assert math.isclose(float(load_result()["d2"]), 108.3, abs_tol=0.11)


def test_d3() -> None:
    assert math.isclose(float(load_result()["d3"]), -2510.3, abs_tol=0.11)
