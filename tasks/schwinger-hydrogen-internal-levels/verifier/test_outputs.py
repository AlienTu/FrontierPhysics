from __future__ import annotations

import functools
import json
import math
import os
import shutil
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eigh_tridiagonal

ROOT = Path(os.environ.get("BENCH_TASK_ROOT", "/root"))
LOGS = Path(os.environ.get("BENCH_VERIFIER_LOGS", "/logs/verifier"))
RATIOS = np.asarray((0.05, 0.10, 0.25, 0.50, 1.00))


def lam_from_ratio(ratio: float) -> float:
    return float(2.0 * np.sqrt(np.pi) * np.exp(np.euler_gamma) * ratio)


def half_profile_first_integral(ratio: float, x: np.ndarray) -> np.ndarray:
    lam = lam_from_ratio(ratio)
    sample_x = np.unique(np.asarray(x, dtype=float))
    assert abs(sample_x[0]) < 1.0e-12
    sample_x[0] = 0.0

    def flow(_x: float, u: np.ndarray) -> np.ndarray:
        radicand = np.maximum(u[0] ** 2 + 2.0 * lam * (1.0 - np.cos(u[0])), 0.0)
        return np.asarray((-np.sqrt(radicand),))

    solution = solve_ivp(
        flow,
        (0.0, float(sample_x[-1])),
        np.asarray((np.pi,)),
        t_eval=sample_x,
        rtol=2.0e-11,
        atol=2.0e-13,
        max_step=0.02,
    )
    assert solution.success
    return np.interp(x, sample_x, solution.y[0])


@functools.lru_cache(maxsize=None)
def independent_spectrum(ratio: float) -> dict[str, object]:
    box = 32.0
    spacing = 0.0125
    x = np.linspace(-box, box, int(round(2.0 * box / spacing)) + 1)
    u = half_profile_first_integral(ratio, np.abs(x))
    phi = np.where(x < 0.0, -u, u - 2.0 * np.pi)
    lam = lam_from_ratio(ratio)
    diagonal = 2.0 / spacing**2 + 1.0 + lam * np.cos(phi[1:-1])
    off_diagonal = -np.ones(diagonal.size - 1) / spacing**2
    eigenvalues = eigh_tridiagonal(
        diagonal,
        off_diagonal,
        select="i",
        select_range=(0, 7),
        check_finite=False,
        eigvals_only=True,
    )
    threshold = float(np.sqrt(1.0 + lam))
    bound = np.sqrt(eigenvalues[(eigenvalues > 1.0e-10) & (eigenvalues < threshold**2)])
    reference = {
        "ratio": ratio,
        "threshold": threshold,
        "frequencies": bound.tolist(),
    }
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / f"reference_{ratio:.2f}.json").write_text(json.dumps(reference, indent=2) + "\n")
    return reference


def load_result() -> dict[str, object]:
    path = ROOT / "atom_spectrum.json"
    assert path.is_file(), "Missing /root/atom_spectrum.json"
    result = json.loads(path.read_text())
    assert set(result) == {"energy_unit", "classification", "levels"}
    assert result["energy_unit"] == "mu=e/sqrt(pi)"
    assert result["classification"] in {
        "localized-internal-levels-present",
        "no-localized-internal-levels",
    }
    assert isinstance(result["levels"], list) and len(result["levels"]) == len(RATIOS)
    return result


def test_artifacts_and_schema_are_complete() -> None:
    result = load_result()
    assert (ROOT / "screening_profile.csv").is_file(), "Missing /root/screening_profile.csv"
    assert (ROOT / "method.md").is_file(), "Missing /root/method.md"
    assert len((ROOT / "method.md").read_text().strip()) >= 120, "method.md is too short to document a convergence check"
    for row, requested_ratio in zip(result["levels"], RATIOS, strict=True):
        assert set(row) == {
            "mass_over_e",
            "continuum_threshold_mu",
            "bound_state_count",
            "bound_frequencies_mu",
            "lowest_binding_gap_mu",
        }
        assert math.isclose(float(row["mass_over_e"]), float(requested_ratio), abs_tol=1.0e-12)
        frequencies = np.asarray(row["bound_frequencies_mu"], dtype=float)
        assert int(row["bound_state_count"]) == frequencies.size
        assert np.isfinite(frequencies).all() and np.all(frequencies > 0.0)
        assert np.all(np.diff(frequencies) > 0.0)
    LOGS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "atom_spectrum.json", LOGS / "submitted_atom_spectrum.json")
    shutil.copy2(ROOT / "screening_profile.csv", LOGS / "submitted_screening_profile.csv")


def test_continuum_thresholds_follow_the_asymptotic_vacuum() -> None:
    rows = load_result()["levels"]
    actual = np.asarray([row["continuum_threshold_mu"] for row in rows], dtype=float)
    expected = np.asarray([independent_spectrum(float(r))["threshold"] for r in RATIOS])
    np.testing.assert_allclose(actual, expected, rtol=2.0e-3, atol=2.0e-4)


def test_internal_level_count_and_frequencies_match_independent_solver() -> None:
    rows = load_result()["levels"]
    any_bound = False
    for row, ratio in zip(rows, RATIOS, strict=True):
        expected = independent_spectrum(float(ratio))
        actual_frequencies = np.asarray(row["bound_frequencies_mu"], dtype=float)
        expected_frequencies = np.asarray(expected["frequencies"], dtype=float)
        assert int(row["bound_state_count"]) == expected_frequencies.size
        np.testing.assert_allclose(actual_frequencies, expected_frequencies, rtol=4.0e-3, atol=8.0e-4)
        any_bound |= bool(expected_frequencies.size)
    expected_classification = (
        "localized-internal-levels-present" if any_bound else "no-localized-internal-levels"
    )
    assert load_result()["classification"] == expected_classification


def test_binding_gaps_are_consistent_and_strictly_below_continuum() -> None:
    for row in load_result()["levels"]:
        frequencies = np.asarray(row["bound_frequencies_mu"], dtype=float)
        threshold = float(row["continuum_threshold_mu"])
        gap = float(row["lowest_binding_gap_mu"])
        if frequencies.size:
            assert np.all(frequencies < threshold)
            assert math.isclose(gap, threshold - frequencies[0], rel_tol=3.0e-3, abs_tol=5.0e-4)
            assert gap > 0.01
        else:
            assert gap == 0.0


def test_screening_profile_matches_field_equations_and_grid() -> None:
    profile = np.genfromtxt(ROOT / "screening_profile.csv", delimiter=",", names=True)
    assert profile.dtype.names == ("xi", "phi", "electric_field_over_e")
    assert profile.shape == (601,)
    expected_x = np.linspace(-12.0, 12.0, 601)
    np.testing.assert_allclose(profile["xi"], expected_x, rtol=0.0, atol=2.0e-10)

    u = half_profile_first_integral(0.25, np.abs(expected_x))
    expected_phi = np.where(expected_x < 0.0, -u, u - 2.0 * np.pi)
    expected_phi[300] = -np.pi
    theta = np.where(expected_x < 0.0, 0.0, np.where(expected_x > 0.0, 1.0, 0.5))
    expected_electric = (expected_phi + 2.0 * np.pi * theta) / (2.0 * np.pi)
    np.testing.assert_allclose(profile["phi"], expected_phi, rtol=2.0e-3, atol=1.5e-3)
    np.testing.assert_allclose(
        profile["electric_field_over_e"],
        expected_electric,
        rtol=3.0e-3,
        atol=5.0e-4,
    )
    np.testing.assert_allclose(profile["phi"] + profile["phi"][::-1], -2.0 * np.pi, atol=2.0e-3)
