from __future__ import annotations

import json
import math
import os
import shutil
from pathlib import Path

ROOT = Path(os.environ.get("BENCH_TASK_ROOT", "/root"))
LOGS = Path(os.environ.get("BENCH_VERIFIER_LOGS", "/logs/verifier"))
COEFFICIENT_ABS_TOLERANCE = 0.05  # Half a unit in the requested decimal place.


def load_result() -> dict[str, object]:
    path = ROOT / "result.json"
    assert path.is_file(), "Missing /root/result.json"
    result = json.loads(path.read_text())
    assert isinstance(result, dict)
    assert set(result) == {"bound_state_exists", "d1", "d2", "d3"}
    assert isinstance(result["bound_state_exists"], bool)
    for name in ("d1", "d2", "d3"):
        assert isinstance(result[name], (int, float))
        assert not isinstance(result[name], bool)
        assert math.isfinite(float(result[name]))
    LOGS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, LOGS / "submitted_result.json")
    return result


def test_result_file_and_schema() -> None:
    load_result()


def test_bound_state_exists() -> None:
    assert load_result()["bound_state_exists"] is True


def test_d1() -> None:
    assert math.isclose(
        float(load_result()["d1"]), 0.0, abs_tol=COEFFICIENT_ABS_TOLERANCE
    )


def test_d2() -> None:
    assert math.isclose(
        float(load_result()["d2"]), 108.3, abs_tol=COEFFICIENT_ABS_TOLERANCE
    )


def test_d3() -> None:
    assert math.isclose(
        float(load_result()["d3"]),
        -2510.4,
        abs_tol=COEFFICIENT_ABS_TOLERANCE,
    )
