# Numerical checks for one-dimensional localized spectra

## Static background

For a canonical scalar with dimensionless static energy

\[
E=\int dx\left[\frac12(\phi')^2+U(\phi,x)\right],
\]

the background satisfies \(-\phi''+\partial_\phi U=0\). Discontinuous external
sources can make \(U\) piecewise-defined while the field and its first
derivative remain continuous. Solve on each smooth region or put source
discontinuities exactly on grid interfaces.

Useful diagnostics are:

- boundary values approach the stated vacua;
- the maximum Euler-Lagrange residual decreases under refinement;
- symmetry identities hold pointwise;
- the static energy stabilizes as the box grows.

## Linear spectrum

For a canonically normalized fluctuation, the Hessian is typically a
Sturm-Liouville operator

\[
L=-\frac{d^2}{dx^2}+U_{\phi\phi}(\phi_{\rm bg},x).
\]

If the two asymptotic vacua have the same curvature \(M_\infty^2\), the
continuum begins at \(\omega=M_\infty\). A finite Dirichlet box always turns the
continuum into discrete levels; do not report those as internal modes.

For every candidate below threshold:

- confirm \(\omega^2>0\);
- compare at two or more box sizes;
- compare at two or more grid spacings;
- inspect that the eigenfunction norm stays concentrated near the defect;
- keep a margin from the continuum edge larger than the observed numerical
  drift.

Second-order finite differences should show approximately quadratic
convergence in the grid spacing when the potential is resolved. Sparse
shift-invert methods and symmetric tridiagonal eigensolvers are both suitable.
