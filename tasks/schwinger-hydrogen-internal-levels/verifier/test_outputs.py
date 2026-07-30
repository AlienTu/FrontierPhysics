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
from scipy.special import sici

ROOT = Path(os.environ.get("BENCH_TASK_ROOT", "/root"))
LOGS = Path(os.environ.get("BENCH_VERIFIER_LOGS", "/logs/verifier"))
RATIOS = np.asarray(
    (0.00025, 0.000375, 0.0005, 0.00075, 0.001, 0.0015, 0.002, 0.003, 0.004),
    dtype=float,
)
SQRT_PI = float(np.sqrt(np.pi))
EULER_GAMMA = float(np.euler_gamma)
CI_PI = float(sici(np.pi)[1])
WEAK_CONSTANT = EULER_GAMMA + np.log(np.pi) - CI_PI


def kappa_squared(mass_over_e: float) -> float:
    return float(np.exp(EULER_GAMMA) * mass_over_e / SQRT_PI)


def half_background_from_first_integral(
    mass_over_e: float, absolute_x: np.ndarray
) -> np.ndarray:
    kappa2 = kappa_squared(mass_over_e)
    samples = np.unique(np.asarray(absolute_x, dtype=float))
    if samples[0] < 1.0e-12:
        samples[0] = 0.0

    def first_order(_x: float, u: np.ndarray) -> np.ndarray:
        radicand = (
            u[0] ** 2
            + kappa2 * (1.0 - np.cos(2.0 * SQRT_PI * u[0]))
        )
        return np.asarray((-np.sqrt(max(radicand, 0.0)),))

    solution = solve_ivp(
        first_order,
        (0.0, float(samples[-1])),
        np.asarray((0.5 * SQRT_PI,)),
        t_eval=samples,
        rtol=2.0e-11,
        atol=2.0e-13,
        max_step=0.03,
    )
    assert solution.success
    return np.interp(absolute_x, samples, solution.y[0])


@functools.lru_cache(maxsize=None)
def independent_reference(mass_over_e: float) -> dict[str, float]:
    kappa2 = kappa_squared(mass_over_e)
    threshold_squared = 1.0 + 2.0 * np.pi * kappa2
    inverse_length = WEAK_CONSTANT * 2.0 * np.pi * kappa2
    half_box = float(max(180.0, 17.0 / inverse_length))

    squared_values: list[float] = []
    second_frequency = None
    for target_spacing in (0.05, 0.025):
        point_count = int(np.ceil(2.0 * half_box / target_spacing)) + 1
        if point_count % 2 == 0:
            point_count += 1
        x = np.linspace(-half_box, half_box, point_count)
        spacing = float(x[1] - x[0])
        absolute_x = np.abs(x)

        u = np.zeros_like(x)
        mask = absolute_x <= 32.0
        u[mask] = half_background_from_first_integral(
            mass_over_e, absolute_x[mask]
        )
        phi = np.where(x < 0.0, -u, u - SQRT_PI)
        potential = (
            1.0
            + 2.0
            * np.pi
            * kappa2
            * np.cos(2.0 * SQRT_PI * phi[1:-1])
        )
        diagonal = 2.0 / spacing**2 + potential
        off_diagonal = -np.ones(diagonal.size - 1) / spacing**2
        eigenvalues = eigh_tridiagonal(
            diagonal,
            off_diagonal,
            select="i",
            select_range=(0, 1),
            eigvals_only=True,
            check_finite=False,
        )
        squared_values.append(float(eigenvalues[0]))
        if target_spacing == 0.025:
            second_frequency = float(np.sqrt(eigenvalues[1]))

    internal_squared = (4.0 * squared_values[1] - squared_values[0]) / 3.0
    squared_gap = float(threshold_squared - internal_squared)
    assert second_frequency is not None

    reference = {
        "mass_over_e": mass_over_e,
        "threshold_squared": threshold_squared,
        "internal_squared": internal_squared,
        "squared_gap": squared_gap,
        "second_box_squared": second_frequency**2,
        "box_half_length": half_box,
    }
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / f"reference_{mass_over_e:.6f}.json").write_text(
        json.dumps(reference, indent=2) + "\n"
    )
    return reference


def load_curve() -> np.ndarray:
    path = ROOT / "spectral_gap_curve.csv"
    assert path.is_file(), "Missing /root/spectral_gap_curve.csv"
    curve = np.genfromtxt(path, delimiter=",", names=True)
    assert curve.dtype.names == (
        "mass_over_e",
        "continuum_threshold_squared_mu2",
        "internal_frequency_squared_mu2",
        "squared_frequency_gap_mu2",
        "gap_over_r_squared",
    )
    assert curve.shape == (len(RATIOS),)
    return curve


def load_asymptotics() -> dict[str, object]:
    path = ROOT / "asymptotics.json"
    assert path.is_file(), "Missing /root/asymptotics.json"
    result = json.loads(path.read_text())
    assert set(result) == {
        "squared_frequency_unit",
        "internal_level_exists",
        "leading_power",
        "leading_coefficient",
        "next_power",
        "next_coefficient",
        "fit_mass_ratio_max",
    }
    assert result["squared_frequency_unit"] == "mu^2=e^2/pi"
    return result


def test_artifacts_and_schema_are_complete() -> None:
    curve = load_curve()
    asymptotics = load_asymptotics()
    assert (ROOT / "report.md").is_file(), "Missing /root/report.md"
    assert len((ROOT / "report.md").read_text().strip()) >= 300
    np.testing.assert_allclose(curve["mass_over_e"], RATIOS, rtol=0.0, atol=1.0e-12)
    for name in curve.dtype.names:
        assert np.isfinite(curve[name]).all(), f"Non-finite values in {name}"
    assert isinstance(asymptotics["internal_level_exists"], bool)
    LOGS.mkdir(parents=True, exist_ok=True)
    for filename in ("spectral_gap_curve.csv", "asymptotics.json", "report.md"):
        shutil.copy2(ROOT / filename, LOGS / f"submitted_{filename}")


def test_squared_thresholds_match_the_asymptotic_vacuum() -> None:
    curve = load_curve()
    expected = np.asarray(
        [
            independent_reference(float(ratio))["threshold_squared"]
            for ratio in RATIOS
        ]
    )
    np.testing.assert_allclose(
        curve["continuum_threshold_squared_mu2"],
        expected,
        rtol=2.0e-4,
        atol=2.0e-7,
    )


def test_internal_squared_frequencies_match_independent_background_solver() -> None:
    curve = load_curve()
    expected = np.asarray(
        [
            independent_reference(float(ratio))["internal_squared"]
            for ratio in RATIOS
        ]
    )
    np.testing.assert_allclose(
        curve["internal_frequency_squared_mu2"],
        expected,
        rtol=3.0e-5,
        atol=2.0e-7,
    )


def test_squared_frequency_gaps_are_positive_and_consistent() -> None:
    curve = load_curve()
    submitted_gap = curve["squared_frequency_gap_mu2"]
    derived_gap = (
        curve["continuum_threshold_squared_mu2"]
        - curve["internal_frequency_squared_mu2"]
    )
    assert np.all(submitted_gap > 0.0)
    np.testing.assert_allclose(
        submitted_gap, derived_gap, rtol=3.0e-4, atol=2.0e-10
    )
    np.testing.assert_allclose(
        curve["gap_over_r_squared"],
        submitted_gap / RATIOS**2,
        rtol=3.0e-4,
        atol=2.0e-4,
    )


def test_squared_gap_curve_matches_independent_large_box_spectra() -> None:
    curve = load_curve()
    expected = np.asarray(
        [
            independent_reference(float(ratio))["squared_gap"]
            for ratio in RATIOS
        ]
    )
    np.testing.assert_allclose(
        curve["squared_frequency_gap_mu2"],
        expected,
        rtol=2.5e-2,
        atol=2.0e-8,
    )
    for ratio in RATIOS[:5]:
        reference = independent_reference(float(ratio))
        assert reference["second_box_squared"] > reference["threshold_squared"]
        relative_offset = (
            reference["second_box_squared"]
            / reference["threshold_squared"]
            - 1.0
        )
        assert relative_offset < 2.0e-5


def test_asymptotic_power_and_coefficients() -> None:
    result = load_asymptotics()
    assert result["internal_level_exists"] is True
    assert int(result["leading_power"]) == 2
    assert int(result["next_power"]) == 3

    leading = float(result["leading_coefficient"])
    correction = float(result["next_coefficient"])
    analytic_leading = float(
        4.0
        * np.pi
        * np.exp(2.0 * EULER_GAMMA)
        * WEAK_CONSTANT**2
    )
    independent_gaps = np.asarray(
        [
            independent_reference(float(ratio))["squared_gap"]
            for ratio in RATIOS[:6]
        ]
    )
    independent_scaled = independent_gaps / RATIOS[:6] ** 2
    independent_polynomial = np.polyfit(
        RATIOS[:6], independent_scaled, 3
    )
    independent_correction = float(independent_polynomial[-2])
    assert math.isclose(leading, analytic_leading, rel_tol=0.035, abs_tol=0.5)
    assert math.isclose(
        correction, independent_correction, rel_tol=0.12, abs_tol=80.0
    )
    fit_max = float(result["fit_mass_ratio_max"])
    assert RATIOS[3] <= fit_max <= RATIOS[6]

    curve = load_curve()
    local_slope = np.polyfit(
        np.log(RATIOS[:5]),
        np.log(curve["squared_frequency_gap_mu2"][:5]),
        1,
    )[0]
    assert 1.94 < local_slope < 2.02
