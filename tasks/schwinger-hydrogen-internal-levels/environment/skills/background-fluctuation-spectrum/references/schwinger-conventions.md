# Schwinger-model conventions and numerical checks

With Coleman normal ordering at

\[
g=\frac{e}{\sqrt{\pi}},
\]

define

\[
\kappa^2=\frac{e^\gamma}{\pi}mg.
\]

For a positive external unit charge at the origin, an equivalent scalar
Hamiltonian is

\[
\mathcal H =
\frac12\Pi^2+\frac12(\partial_x\phi)^2
+\frac12g^2\left(\phi+\sqrt{\pi}\Theta(x)\right)^2
+\frac{\kappa^2}{2}\left[1-\cos(2\sqrt{\pi}\phi)\right].
\]

The screened static sector obeys

\[
\phi(-\infty)=0,\qquad \phi(+\infty)=-\sqrt{\pi}.
\]

At \(\theta=0\), reflection and charge conjugation give

\[
\phi(-x)=-\sqrt{\pi}-\phi(x),\qquad \phi(0)=-\frac{\sqrt{\pi}}{2}.
\]

The static equation away from the source is

\[
-\phi''+
g^2\left(\phi+\sqrt{\pi}\Theta(x)\right)
+\sqrt{\pi}\kappa^2\sin(2\sqrt{\pi}\phi)=0.
\]

The canonically normalized fluctuation operator is

\[
\mathcal K=
-\frac{d^2}{dx^2}
+g^2+2\pi\kappa^2\cos(2\sqrt{\pi}\phi_{\rm bg}(x)).
\]

Its infinite-volume continuum threshold is

\[
\omega_{\rm th}=\sqrt{g^2+2\pi\kappa^2}.
\]

The most stable weak-binding observable is the direct eigenvalue difference

\[
\Delta_B=\omega_{\rm th}^2-\omega_{\rm int}^2.
\]

Use this squared-frequency gap for asymptotic fitting. The ordinary binding
energy can be recovered, if desired, from

\[
\omega_{\rm th}-\omega_{\rm int}
=\frac{\Delta_B}{\omega_{\rm th}+\omega_{\rm int}}.
\]

In units \(g=1\), the input ratio \(r=m/e\) implies

\[
\frac{\kappa^2}{g^2}=\frac{e^\gamma}{\sqrt{\pi}}r.
\]

For a second-order finite-difference operator, compare at least two grid
spacings and use the observed \(h^2\) behavior to extrapolate the lowest
eigenvalue. In a Dirichlet box, the first continuum eigenvalue lies slightly
above \(\omega_{\rm th}\) and approaches it algebraically with box size. A
localized state below threshold converges exponentially once the box is many
decay lengths wide.
