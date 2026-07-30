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
  - csv
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

Evaluate

\[
r\in\{
0.00025,\ 0.000375,\ 0.0005,\ 0.00075,\ 0.001,\ 0.0015,\
0.002,\ 0.003,\ 0.004
\}.
\]

Use the computed weak-mass curve to determine the first two nonzero terms

\[
\frac{\Delta_B(r)}{\mu^2}
=d_p r^p+d_{p+1}r^{p+1}+o(r^{p+1}),
\]

without assuming \(p\) in advance. Report the integer leading power \(p\), its
coefficient \(d_p\), and the first correction coefficient \(d_{p+1}\).

Write `/root/spectral_gap_curve.csv` with exactly this header:

```text
mass_over_e,continuum_threshold_squared_mu2,internal_frequency_squared_mu2,squared_frequency_gap_mu2,gap_over_r_squared
```

Include exactly the nine requested mass ratios in increasing order. All
squared frequencies are in units of \(\mu^2\). Retain enough digits to resolve
the smallest squared-frequency gap.

Write `/root/asymptotics.json` with exactly this structure:

```json
{
  "squared_frequency_unit": "mu^2=e^2/pi",
  "internal_level_exists": true,
  "leading_power": 0,
  "leading_coefficient": 0.0,
  "next_power": 0,
  "next_coefficient": 0.0,
  "fit_mass_ratio_max": 0.0
}
```

Set `internal_level_exists` from the infinite-volume result, not from the
presence of a finite-box eigenvalue. Set `fit_mass_ratio_max` to the largest
mass ratio included in the asymptotic coefficient fit.

Finally, write `/root/report.md`. State the physical criterion used to
distinguish the localized mode from the continuum, document at least two box
sizes and two spatial resolutions, and show how the inferred asymptotic
coefficients change under at least two fit windows. The scientific result,
rather than the choice of method or software, will be graded.
