---
name: background-fluctuation-spectrum
description: Compute localized semiclassical excitation spectra around static one-dimensional scalar-field backgrounds with controlled continuum and finite-volume diagnostics.
---

# Background and fluctuation spectra

Use this workflow when a field theory problem asks whether a static defect,
screening cloud, soliton, or impurity supports localized small excitations.

1. Nondimensionalize before discretizing. Derive the static Euler-Lagrange
   equation and both asymptotic vacua from the supplied Hamiltonian.
2. Exploit exact reflection or charge-conjugation symmetries when they exist.
   Solve the nonlinear background as a boundary-value problem and verify its
   residual independently.
3. Form the second variation of the energy about that background. Put the
   kinetic term in canonical normalization before interpreting eigenvalues as
   squared frequencies.
4. Determine the continuum edge from the asymptotic fluctuation operator, not
   from the largest computed eigenvalue.
5. Solve only for the low end of the self-adjoint spectrum. A physical
   localized mode must have positive squared frequency, lie below the
   continuum edge, and remain normalizable as the box grows.
6. Repeat at larger boxes and finer grids. Track eigenvalues and localization
   measures rather than relying on the number of finite-box eigenvectors.
7. Reconstruct physical observables from the background using the conventions
   in the problem statement.

Read `references/numerical-checks.md` before finalizing the spectrum.
