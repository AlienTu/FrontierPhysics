---
schema_version: '1.3'
metadata:
  author_name: Haochen Tu
  author_email: at5526@princeton.edu
  difficulty: hard
  category: natural-science
  subcategory: quantum-field-theory
  category_confidence: high
  task_type:
  - analysis
  - calculation
  - simulation
  modality:
  - scientific-data
  - json
  interface:
  - terminal
  - python
  skill_type:
  - domain-procedure
  - mathematical-method
  - library-api-usage
  tags:
  - theoretical-physics
  - quantum-electrodynamics
  - schwinger-model
  - weak-binding
  - spectral-analysis
verifier:
  type: test-script
  timeout_sec: 900.0
  service: main
  pytest_plugins:
  - ctrf
  hardening:
    cleanup_conftests: true
agent:
  timeout_sec: 7200.0
environment:
  network_mode: no-network
  build_timeout_sec: 1200.0
  os: linux
  cpus: 4
  memory_mb: 8192
  storage_mb: 10240
  gpus: 0
---

Consider one-flavour massive QED in \(1+1\) dimensions,

\[
\mathcal L=
-\frac14F_{\mu\nu}F^{\mu\nu}
+\bar\psi(i\gamma^\mu D_\mu-m)\psi
-A_\mu j^\mu_{\mathrm{ext}},
\qquad
j^0_{\mathrm{ext}}(x)=e\,\delta(x),\quad
j^1_{\mathrm{ext}}(x)=0.
\]

The external source is an infinitely heavy positive unit charge fixed at the
origin. Work at zero background electrical field, on the infinite line, in the neutral sector in
which the external charge is completely screened by the dynamical field. This
is the \(1+1\)-dimensional analogue of a hydrogen atom.

Determine, at leading semiclassical order, whether the screened atom has a
localized neutral internal excitation when \(m/e\ll1\). You may use any
equivalent analytical or numerical formulation; no particular field
variables, transformation, or computational method are prescribed.

Use

\[
\mu=\frac{e}{\sqrt{\pi}}
\]

as the energy unit. For each mass ratio \(r=m/e\), define:

- \(\omega_{\mathrm{th}}(r)\), the lowest neutral scattering threshold;
- \(\omega_{\mathrm{int}}(r)\), the lowest positive-frequency normalizable
  excitation localized near the external charge;
- \(\Delta_B(r)=\omega_{\mathrm{th}}^2(r)-\omega_{\mathrm{int}}^2(r)\),
  the squared-frequency gap below the scattering threshold.

A finite-box continuum eigenvalue is not an internal level. Count a mode only
if it remains below the infinite-volume threshold and localized near the
source as the box and numerical resolution are increased.

Determine the first two terms of the weak-mass expansion

\[
\frac{\Delta_B(r)}{\mu^2}
=d_2 r^2+d_3r^3+o(r^3).
\]

You may determine the coefficients analytically, numerically, or by a
combination of the two. Write `/root/result.json` with exactly this structure:

```json
{
  "d2": 0.0,
  "d3": 0.0
}
```

Report both coefficients to one decimal place. The scientific result, rather
than the choice of field variables, derivation, numerical method, or software,
will be graded.
