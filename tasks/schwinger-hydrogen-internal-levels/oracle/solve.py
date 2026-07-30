#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

ROOT = Path(os.environ.get("BENCH_TASK_ROOT", "/root"))
RATIOS = (0.05, 0.10, 0.25, 0.50, 1.00)
EULER_GAMMA = float(np.euler_gamma)


def coupling(mass_over_e: float) -> float:
    return 2.0 * np.sqrt(np.pi) * np.exp(EULER_GAMMA) * mass_over_e


def positive_half_background(mass_over_e: float, box: float, points: int):
    lam = coupling(mass_over_e)
    x = np.linspace(0.0, box, points)
    scale = np.sqrt(1.0 + lam)
    phi_guess = -2.0 * np.pi + np.pi * np.exp(-scale * x)
    y_guess = np.vstack((phi_guess, np.gradient(phi_guess, x)))

    def equation(_x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return np.vstack((y[1], y[0] + 2.0 * np.pi + lam * np.sin(y[0])))

    def boundary(left: np.ndarray, right: np.ndarray) -> np.ndarray:
        return np.asarray((left[0] + np.pi, right[0] + 2.0 * np.pi))

    solution = solve_bvp(
        equation,
        boundary,
        x,
        y_guess,
        tol=2.0e-10,
        max_nodes=50_000,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution


def full_background(solution, box: float, points: int) -> tuple[np.ndarray, np.ndarray]:
    x_positive = np.linspace(0.0, box, points)
    phi_positive = solution.sol(x_positive)[0]
    x = np.concatenate((-x_positive[:0:-1], x_positive))
    phi = np.concatenate((-2.0 * np.pi - phi_positive[:0:-1], phi_positive))
    return x, phi


def low_spectrum(mass_over_e: float, box: float, half_points: int) -> tuple[np.ndarray, float]:
    lam = coupling(mass_over_e)
    solution = positive_half_background(mass_over_e, box, half_points)
    x, phi = full_background(solution, box, half_points)
    spacing = x[1] - x[0]
    potential = 1.0 + lam * np.cos(phi[1:-1])
    dimension = potential.size
    operator = diags(
        (
            -np.ones(dimension - 1) / spacing**2,
            2.0 / spacing**2 + potential,
            -np.ones(dimension - 1) / spacing**2,
        ),
        offsets=(-1, 0, 1),
        format="csc",
    )
    eigenvalues = np.sort(eigsh(operator, k=8, which="SA", return_eigenvectors=False))
    threshold_squared = 1.0 + lam
    bound = eigenvalues[(eigenvalues > 1.0e-9) & (eigenvalues < threshold_squared)]
    return np.sqrt(bound), float(np.sqrt(threshold_squared))


def converged_level(mass_over_e: float) -> tuple[np.ndarray, float, dict[str, float]]:
    coarse, coarse_threshold = low_spectrum(mass_over_e, box=24.0, half_points=1601)
    fine, threshold = low_spectrum(mass_over_e, box=30.0, half_points=2401)
    if coarse.size != fine.size:
        raise RuntimeError(f"Bound-state count did not converge for m/e={mass_over_e}")
    drift = float(np.max(np.abs(coarse - fine))) if fine.size else 0.0
    if drift > 2.0e-3 or abs(coarse_threshold - threshold) > 1.0e-12:
        raise RuntimeError(f"Spectrum did not converge for m/e={mass_over_e}")
    return fine, threshold, {"coarse_box": 24.0, "fine_box": 30.0, "max_frequency_drift": drift}


def write_profile() -> None:
    ratio = 0.25
    solution = positive_half_background(ratio, box=30.0, points=2401)
    xi = np.linspace(-12.0, 12.0, 601)
    absolute_x = np.abs(xi)
    right_phi = solution.sol(absolute_x)[0]
    phi = np.where(xi < 0.0, -2.0 * np.pi - right_phi, right_phi)
    theta = np.where(xi < 0.0, 0.0, np.where(xi > 0.0, 1.0, 0.5))
    electric_field = (phi + 2.0 * np.pi * theta) / (2.0 * np.pi)
    table = np.column_stack((xi, phi, electric_field))
    np.savetxt(
        ROOT / "screening_profile.csv",
        table,
        delimiter=",",
        header="xi,phi,electric_field_over_e",
        comments="",
        fmt="%.12g",
    )


def main() -> None:
    rows = []
    convergence = {}
    for ratio in RATIOS:
        frequencies, threshold, diagnostics = converged_level(ratio)
        rows.append(
            {
                "mass_over_e": ratio,
                "continuum_threshold_mu": threshold,
                "bound_state_count": int(frequencies.size),
                "bound_frequencies_mu": frequencies.tolist(),
                "lowest_binding_gap_mu": float(threshold - frequencies[0]) if frequencies.size else 0.0,
            }
        )
        convergence[str(ratio)] = diagnostics

    result = {
        "energy_unit": "mu=e/sqrt(pi)",
        "classification": "localized-internal-levels-present"
        if any(row["bound_state_count"] for row in rows)
        else "no-localized-internal-levels",
        "levels": rows,
    }
    (ROOT / "atom_spectrum.json").write_text(json.dumps(result, indent=2) + "\n")
    write_profile()
    (ROOT / "method.md").write_text(
        "# Method\n\n"
        "I minimized the static screened sector as a nonlinear boundary-value "
        "problem and diagonalized the canonically normalized second variation. "
        "A mode was counted only when its positive frequency remained below the "
        "asymptotic continuum edge as the box and grid were enlarged.\n\n"
        "## Convergence\n\n```json\n"
        + json.dumps(convergence, indent=2)
        + "\n```\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
