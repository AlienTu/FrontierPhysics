#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp
from scipy.linalg import eigh_tridiagonal
from scipy.special import sici

ROOT = Path(os.environ.get("BENCH_TASK_ROOT", "/root"))
RATIOS = np.asarray(
    (0.00025, 0.000375, 0.0005, 0.00075, 0.001, 0.0015, 0.002, 0.003, 0.004),
    dtype=float,
)
SQRT_PI = float(np.sqrt(np.pi))
EULER_GAMMA = float(np.euler_gamma)
CI_PI = float(sici(np.pi)[1])
WEAK_DECAY_CONSTANT = float(EULER_GAMMA + np.log(np.pi) - CI_PI)


@dataclass(frozen=True)
class SpectralResult:
    ratio: float
    threshold: float
    internal_frequency: float
    binding_energy: float
    coarse_internal_squared: float
    fine_internal_squared: float
    second_box_frequency: float
    box_half_length: float
    coarse_spacing: float
    fine_spacing: float


def kappa_squared_over_g_squared(mass_over_e: float) -> float:
    # g=e/sqrt(pi), kappa^2=e^gamma*m*g/pi.
    return float(np.exp(EULER_GAMMA) * mass_over_e / SQRT_PI)


def solve_positive_half_background(mass_over_e: float):
    kappa_squared = kappa_squared_over_g_squared(mass_over_e)
    threshold_squared = 1.0 + 2.0 * np.pi * kappa_squared
    x = np.linspace(0.0, 30.0, 3001)
    u_guess = 0.5 * SQRT_PI * np.exp(-np.sqrt(threshold_squared) * x)
    y_guess = np.vstack((u_guess, np.gradient(u_guess, x)))

    # u=phi+sqrt(pi) on x>0, so u(0)=sqrt(pi)/2 and u(infinity)=0.
    def equation(_x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return np.vstack(
            (
                y[1],
                y[0]
                + SQRT_PI
                * kappa_squared
                * np.sin(2.0 * SQRT_PI * y[0]),
            )
        )

    def boundary(left: np.ndarray, right: np.ndarray) -> np.ndarray:
        return np.asarray((left[0] - 0.5 * SQRT_PI, right[0]))

    solution = solve_bvp(
        equation,
        boundary,
        x,
        y_guess,
        tol=1.0e-11,
        max_nodes=40_000,
    )
    if not solution.success:
        raise RuntimeError(f"Background solve failed: {solution.message}")
    return solution


def lowest_two_squared(
    solution,
    kappa_squared: float,
    box_half_length: float,
    target_spacing: float,
) -> tuple[np.ndarray, float]:
    point_count = int(np.ceil(2.0 * box_half_length / target_spacing)) + 1
    if point_count % 2 == 0:
        point_count += 1
    x = np.linspace(-box_half_length, box_half_length, point_count)
    spacing = float(x[1] - x[0])
    absolute_x = np.abs(x)

    u = np.zeros_like(x)
    background_region = absolute_x <= 30.0
    u[background_region] = solution.sol(absolute_x[background_region])[0]
    phi = np.where(x < 0.0, -u, u - SQRT_PI)

    potential = (
        1.0
        + 2.0
        * np.pi
        * kappa_squared
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
    return eigenvalues, spacing


def solve_ratio(mass_over_e: float) -> SpectralResult:
    kappa_squared = kappa_squared_over_g_squared(mass_over_e)
    threshold_squared = 1.0 + 2.0 * np.pi * kappa_squared
    threshold = float(np.sqrt(threshold_squared))
    weak_inverse_length = (
        WEAK_DECAY_CONSTANT * 2.0 * np.pi * kappa_squared
    )
    box_half_length = float(max(160.0, 16.0 / weak_inverse_length))
    solution = solve_positive_half_background(mass_over_e)

    coarse_values, coarse_spacing = lowest_two_squared(
        solution, kappa_squared, box_half_length, 0.04
    )
    fine_values, fine_spacing = lowest_two_squared(
        solution, kappa_squared, box_half_length, 0.02
    )

    # Second-order finite differences: extrapolate the bound eigenvalue in h^2.
    internal_squared = float((4.0 * fine_values[0] - coarse_values[0]) / 3.0)
    if not 0.0 < internal_squared < threshold_squared:
        raise RuntimeError(f"No converged sub-threshold mode for m/e={mass_over_e}")
    internal_frequency = float(np.sqrt(internal_squared))
    binding_energy = float(threshold - internal_frequency)

    second_box_frequency = float(np.sqrt(fine_values[1]))
    if second_box_frequency <= threshold:
        raise RuntimeError(
            f"Second finite-box eigenvalue fell below threshold for m/e={mass_over_e}"
        )

    return SpectralResult(
        ratio=mass_over_e,
        threshold=threshold,
        internal_frequency=internal_frequency,
        binding_energy=binding_energy,
        coarse_internal_squared=float(coarse_values[0]),
        fine_internal_squared=float(fine_values[0]),
        second_box_frequency=second_box_frequency,
        box_half_length=box_half_length,
        coarse_spacing=coarse_spacing,
        fine_spacing=fine_spacing,
    )


def infer_asymptotics(results: list[SpectralResult]) -> tuple[dict[str, object], dict[str, object]]:
    ratios = np.asarray([result.ratio for result in results])
    bindings = np.asarray([result.binding_energy for result in results])

    # Infer the leading power from the smallest five points before fitting
    # coefficients. Rounding is justified by the requested integer-power expansion.
    log_slope = float(
        np.polyfit(np.log(ratios[:5]), np.log(bindings[:5]), 1)[0]
    )
    leading_power = int(round(log_slope))
    if leading_power < 1:
        raise RuntimeError("Failed to infer a positive leading power")

    window_diagnostics: dict[str, object] = {}
    selected_coefficients = None
    selected_max_ratio = None
    for window_size in (4, 5, 6, 7):
        x = ratios[:window_size]
        scaled = bindings[:window_size] / x**leading_power
        # The intercept and linear term are c_p and c_{p+1}. Higher terms
        # stabilize the extrapolation without fixing their values.
        polynomial = np.polyfit(x, scaled, 3)
        leading_coefficient = float(polynomial[-1])
        next_coefficient = float(polynomial[-2])
        window_diagnostics[str(window_size)] = {
            "fit_mass_ratio_max": float(x[-1]),
            "leading_coefficient": leading_coefficient,
            "next_coefficient": next_coefficient,
        }
        if window_size == 6:
            selected_coefficients = (leading_coefficient, next_coefficient)
            selected_max_ratio = float(x[-1])

    assert selected_coefficients is not None and selected_max_ratio is not None
    asymptotics = {
        "energy_unit": "mu=e/sqrt(pi)",
        "internal_level_exists": True,
        "leading_power": leading_power,
        "leading_coefficient": selected_coefficients[0],
        "next_power": leading_power + 1,
        "next_coefficient": selected_coefficients[1],
        "fit_mass_ratio_max": selected_max_ratio,
    }
    diagnostics = {
        "local_log_log_slope": log_slope,
        "fit_windows": window_diagnostics,
    }
    return asymptotics, diagnostics


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    results = [solve_ratio(float(ratio)) for ratio in RATIOS]
    asymptotics, fit_diagnostics = infer_asymptotics(results)

    representative = results[4]  # m/e=0.001
    representative_kappa_squared = kappa_squared_over_g_squared(
        representative.ratio
    )
    representative_background = solve_positive_half_background(
        representative.ratio
    )
    box_size_check = []
    for box_fraction in (0.75, 1.0):
        checked_half_length = box_fraction * representative.box_half_length
        checked_values, checked_spacing = lowest_two_squared(
            representative_background,
            representative_kappa_squared,
            checked_half_length,
            0.025,
        )
        box_size_check.append(
            {
                "mass_over_e": representative.ratio,
                "box_half_length": checked_half_length,
                "spacing": checked_spacing,
                "lowest_frequency": float(np.sqrt(checked_values[0])),
                "second_frequency": float(np.sqrt(checked_values[1])),
            }
        )

    curve = np.asarray(
        [
            (
                result.ratio,
                result.threshold,
                result.internal_frequency,
                result.binding_energy,
                result.binding_energy / result.ratio**2,
            )
            for result in results
        ]
    )
    np.savetxt(
        ROOT / "binding_curve.csv",
        curve,
        delimiter=",",
        header=(
            "mass_over_e,continuum_threshold_mu,internal_frequency_mu,"
            "binding_energy_mu,binding_over_r_squared"
        ),
        comments="",
        fmt="%.14g",
    )
    (ROOT / "asymptotics.json").write_text(
        json.dumps(asymptotics, indent=2) + "\n"
    )

    spectral_diagnostics = [
        {
            "mass_over_e": result.ratio,
            "box_half_length": result.box_half_length,
            "coarse_spacing": result.coarse_spacing,
            "fine_spacing": result.fine_spacing,
            "coarse_internal_squared": result.coarse_internal_squared,
            "fine_internal_squared": result.fine_internal_squared,
            "second_box_frequency": result.second_box_frequency,
            "continuum_threshold": result.threshold,
            "second_threshold_relative_error": (
                result.second_box_frequency / result.threshold - 1.0
            ),
        }
        for result in results
    ]
    diagnostics = {
        "conventions": {
            "g": "e/sqrt(pi)",
            "kappa_squared": "exp(gamma)*m*g/pi",
            "threshold_squared": "g^2+2*pi*kappa^2",
        },
        "spectra": spectral_diagnostics,
        "box_size_check": box_size_check,
        **fit_diagnostics,
    }
    (ROOT / "oracle_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2) + "\n"
    )

    windows = fit_diagnostics["fit_windows"]
    report_lines = [
        "# Weakly bound internal mode",
        "",
        "The lowest positive fluctuation eigenvalue remains below the asymptotic "
        "neutral scattering threshold as the box is enlarged. The next "
        "finite-box eigenvalue approaches the threshold from above, while the "
        "sub-threshold eigenfunction has an exponentially decaying tail.",
        "",
        "## Numerical convergence",
        "",
        "For every mass ratio I used a half-box at least sixteen estimated "
        "decay lengths wide. I diagonalized the symmetric tridiagonal "
        "fluctuation operator at target spacings 0.04 and 0.02 and used the "
        "observed second-order grid behavior to extrapolate the lowest squared "
        "frequency.",
        "",
        "At m/e=0.001 I also repeated the calculation at two half-box lengths:",
        "",
        "| half-box | spacing | lowest frequency | second frequency |",
        "|---:|---:|---:|---:|",
    ]
    for item in box_size_check:
        report_lines.append(
            f"| {item['box_half_length']:.9g} | {item['spacing']:.9g} | "
            f"{item['lowest_frequency']:.12g} | "
            f"{item['second_frequency']:.12g} |"
        )
    report_lines.extend(
        [
        "",
        "The first frequency is stable while the second finite-box frequency "
        "moves toward the analytic scattering threshold from above. Full "
        "diagnostics are saved in `oracle_diagnostics.json`.",
        "",
        "## Fit-window stability",
        "",
        "| points | max m/e | leading coefficient | next coefficient |",
        "|---:|---:|---:|---:|",
        ]
    )
    for size in (4, 5, 6, 7):
        item = windows[str(size)]
        report_lines.append(
            f"| {size} | {item['fit_mass_ratio_max']:.7g} | "
            f"{item['leading_coefficient']:.9g} | "
            f"{item['next_coefficient']:.9g} |"
        )
    report_lines.extend(
        [
            "",
            f"The local small-mass log-log slope is "
            f"{fit_diagnostics['local_log_log_slope']:.9g}.",
            "",
        ]
    )
    (ROOT / "report.md").write_text("\n".join(report_lines))
    print(json.dumps(asymptotics, indent=2))


if __name__ == "__main__":
    main()
