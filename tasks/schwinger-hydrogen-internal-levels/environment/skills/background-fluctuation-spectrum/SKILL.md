---
name: background-fluctuation-spectrum
description: Derive and compute weakly bound localized modes around screened static charges in one-dimensional field theories, including bosonization conventions, large-box spectral checks, and asymptotic fitting.
---

# Screened backgrounds and weakly bound modes

Use this workflow for a static external charge in the one-flavour Schwinger
model.

1. Translate the fermionic theory to a scalar description using Coleman
   normal ordering at the massless Schwinger scale.
2. Fix all normalization factors before solving. The useful conventions and
   source boundary conditions are in `references/schwinger-conventions.md`.
3. Solve the nonlinear screened background as a boundary-value problem. Use
   reflection symmetry to place the source exactly at a half-domain boundary.
4. Construct the canonically normalized second variation about the background.
5. Diagonalize the symmetric tridiagonal discretization at the bottom of the
   spectrum. The first eigenvalue is a candidate internal mode. The next
   eigenvalue is a useful finite-box estimate of the continuum edge.
6. Increase the box until the first mode is stable and the second eigenvalue
   approaches the analytic asymptotic threshold.
7. Refine the grid and extrapolate the lowest eigenvalue in the grid spacing.
8. Fit the squared-frequency gap directly, before taking square roots. Check
   local log slopes and vary the largest mass ratio retained in the fit.

Do not treat the first discretized continuum state as an internal excitation.
For a very shallow mode, choose the box from the mode's decay length rather
than from the much shorter background-field length scale.
